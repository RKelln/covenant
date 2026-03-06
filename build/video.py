"""
video.py — Render Covenant ritual text as an animated video.

Parses stanzas from dist/covenant.ritual.md, renders overlay frames using
Pillow, and pipes them directly into FFmpeg — no temp files.

The video opens with a title card: the Covenant mark fades in, then the
wordmark "COVENANT" fades in beneath it, the whole card holds, then fades out
before the ritual stanzas begin.

Usage:
    uv run python build/video.py --bg <background_video> [options]

Options:
    --bg PATH           Background video to loop (required)
    --out PATH          Output file [default: dist/covenant_ritual.mp4]
    --ritual PATH       Ritual markdown to parse [default: dist/covenant.ritual.md]
    --fps INT           Frames per second [default: 30]
    --hold FLOAT        Seconds each stanza is fully visible [default: 5.0]
    --fade FLOAT        Fade in / fade out duration in seconds [default: 1.5]
    --gap FLOAT         Silence gap between stanzas in seconds [default: 0.5]
    --title-hold FLOAT  Seconds the title card is fully visible [default: 4.0]
    --title-fade FLOAT  Fade duration for title card elements [default: 1.5]
    --logo-scale FLOAT  Logo height as fraction of frame height [default: 0.22]
    --width INT         Output video width [default: 1920]
    --height INT        Output video height [default: 1080]
    --font-size INT     Base font size in points [default: 72]
    --margin INT        Horizontal margin in pixels [default: 200]
    --color STR         Text colour as hex [default: #f5f0e8]
    --shadow            Add a soft drop shadow behind text
    --darken AMOUNT     Highlight rolloff 0–1: compresses bright pixels down while leaving shadows alone (default 0.0)
    --sections LIST     Comma-separated section IDs to include (default: all)
    --list-sections     Print available section IDs and exit
    --dry-run           Check layout only — print overflowing stanzas in full and exit
    --preview SECS      Render only the first N seconds (for testing)
    --auto-timing       Scale hold time with stanza line count (--hold = secs/line)
    --frames-only DIR   Write PNG frames to DIR and exit (skip FFmpeg, for debugging)

Examples:
    uv run python build/video.py --bg loop.mp4
    uv run python build/video.py --bg loop.mp4 --hold 6 --fade 2 --font-size 80
    uv run python build/video.py --bg loop.mp4 --sections preamble,closing
    uv run python build/video.py --bg loop.mp4 --preview 30 --darken 0.7
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
DIST_DIR = REPO_ROOT / "dist"
FONTS_DIR = REPO_ROOT / "assets" / "fonts"

FONT_REGULAR = FONTS_DIR / "CormorantGaramond-600-normal.ttf"
FONT_ITALIC = FONTS_DIR / "CormorantGaramond-600-italic.ttf"

RITUAL_MD = DIST_DIR / "covenant.ritual.md"
LOGO_PNG = REPO_ROOT / "assets" / "covenant_logo.png"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Stanza:
    """A contiguous block of non-blank lines within a ritual section."""

    section_title: str
    section_id: str
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# Matches lines like:  ## Preamble <a id='preamble'></a>
SECTION_HEADER_RE = re.compile(
    r"^##\s+(.+?)\s+<a\s+id=['\"]([^'\"]+)['\"]", re.IGNORECASE
)

# Lines to skip entirely (top-level heading, meta lines, separators, TOC entries)
# "- " catches markdown list items; "---" catches HR separators.
# Note: bare "-" is intentionally NOT included to avoid matching em-dashes mid-line.
SKIP_PREFIX = ("#", "*", "---", "- ", "[")


def is_skippable(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False  # blank lines are handled separately
    return stripped.startswith(SKIP_PREFIX)


def parse_ritual(path: Path) -> list[Stanza]:
    """Parse ritual markdown into a flat list of Stanza objects."""
    stanzas: list[Stanza] = []
    current_section_title = ""
    current_section_id = ""
    current_lines: list[str] = []

    def flush():
        if current_lines:
            stanzas.append(
                Stanza(
                    section_title=current_section_title,
                    section_id=current_section_id,
                    lines=list(current_lines),
                )
            )
            current_lines.clear()

    text = path.read_text(encoding="utf-8")

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Section header (## with anchor id)
        m = SECTION_HEADER_RE.match(line)
        if m:
            flush()
            current_section_title = m.group(1).strip()
            current_section_id = m.group(2).strip()
            continue

        # Top-level heading (# ...) — marks end of sections (e.g. Credits)
        if re.match(r"^#\s+", line):
            flush()
            current_section_title = ""
            current_section_id = ""
            continue

        # Skip decorative / structural lines
        if is_skippable(line):
            flush()
            continue

        stripped = line.strip()

        if stripped == "":
            # Blank line = stanza boundary
            flush()
        else:
            current_lines.append(stripped)

    flush()

    # Remove empty stanzas and any content before the first real section
    return [s for s in stanzas if any(l.strip() for l in s.lines) and s.section_id]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) not in (6, 8):
        raise ValueError(
            f"Expected a 6- or 8-digit hex colour (got {hex_color!r}). "
            "Use #RRGGBB, RRGGBB, or RRGGBBAA."
        )
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    a = int(h[6:8], 16) if len(h) >= 8 else alpha
    return (r, g, b, a)


def tint_logo(
    logo_path: Path, color_rgb: tuple[int, int, int], scale_height: int
) -> Image.Image:
    """Load the black-on-white logo PNG, recolour it to color_rgb, and scale it.

    The logo is treated as a greyscale mask: black pixels become the target
    colour; white pixels become fully transparent.  This lets it composite
    cleanly over any background.
    """
    src = Image.open(logo_path).convert("RGBA")

    # Scale proportionally to the requested height
    orig_w, orig_h = src.size
    scale = scale_height / orig_h
    new_w = int(orig_w * scale)
    src = src.resize((new_w, scale_height), Image.LANCZOS)

    # Invert brightness: black (0) → opaque, white (255) → transparent
    # Use the luminance of the original pixel as the alpha mask
    grey = src.convert("L")  # luminance
    # Invert so dark pixels are opaque
    alpha_mask = grey.point(lambda px: 255 - px)

    # Build a solid-colour image in the target colour
    coloured = Image.new(
        "RGBA", src.size, (color_rgb[0], color_rgb[1], color_rgb[2], 255)
    )
    coloured.putalpha(alpha_mask)

    return coloured


def render_title_card(
    width: int,
    height: int,
    color_rgba: tuple[int, int, int, int],
    logo_scale: float,
    alpha_logo: float,
    alpha_word: float,
    shadow: bool,
    _prebuilt_logo: Image.Image | None = None,
) -> Image.Image:
    """Render one title-card frame with the mark and wordmark at given alphas.

    The logo PNG already contains both the mark and the wordmark as a single
    designed unit.  We composite it in two passes:

    - Pass 1 (alpha_logo): the full logo at alpha_logo opacity — mark entrance
    - Pass 2 (alpha_word): re-composite just the bottom wordmark strip at the
      delta between alpha_word and alpha_logo, so the wordmark can fade in
      independently while the mark is already visible at full opacity

    In practice:
      Phase 1  alpha_logo ramps 0→1, alpha_word = 0  → mark fades in alone
      Phase 2  alpha_logo = 1,       alpha_word ramps 0→1 → wordmark fades in
      Phase 3  both = 1              → full logo holds
      Phase 4  both ramp 1→0 together → everything fades out

    To achieve independent control without a separate mark asset we simply
    blit the full logo twice:
      - First blit at alpha_logo  (includes both mark and wordmark)
      - Second blit of a wordmark-only crop at (alpha_word - alpha_logo),
        clamped to ≥ 0  — this tops up the wordmark to its target opacity.

    Pass *_prebuilt_logo* to avoid reloading and retinting the logo image on
    every fade frame.  :func:`iter_frames` pre-builds it once and passes it in.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    if not LOGO_PNG.exists():
        return img

    logo_h = int(height * logo_scale)
    color_rgb = (color_rgba[0], color_rgba[1], color_rgba[2])

    # Use pre-built logo if provided, otherwise load and tint now.
    full_logo = (
        _prebuilt_logo
        if _prebuilt_logo is not None
        else tint_logo(LOGO_PNG, color_rgb, logo_h)
    )
    logo_w, logo_h_actual = full_logo.size

    # Centre position
    lx = (width - logo_w) // 2
    ly = (height - logo_h_actual) // 2

    # --- Pass 1: full logo at alpha_logo ---
    if alpha_logo > 0:
        lo = scale_alpha(full_logo, alpha_logo)
        img.paste(lo, (lx, ly), lo)

    # --- Pass 2: wordmark strip top-up ---
    # The wordmark occupies roughly the bottom 30 % of the logo image.
    # We crop that strip and blit it at the extra opacity needed.
    extra = alpha_word - alpha_logo
    if extra > 0:
        strip_top = int(logo_h_actual * 0.68)  # empirical: wordmark starts ~68 % down
        wm_strip = full_logo.crop((0, strip_top, logo_w, logo_h_actual))
        wm_strip = scale_alpha(wm_strip, extra)
        img.paste(wm_strip, (lx, ly + strip_top), wm_strip)

    return img


def wrap_lines(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    wrapped: list[str] = []
    for raw_line in text.splitlines():
        words = raw_line.split()
        if not words:
            wrapped.append("")
            continue
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            bbox = font.getbbox(test)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current = test
            else:
                if current:
                    wrapped.append(current)
                current = word
        if current:
            wrapped.append(current)
    return wrapped


def check_stanzas_fit(
    stanzas: list[Stanza],
    width: int,
    height: int,
    font_size: int,
    margin: int,
) -> list[tuple[Stanza, str]]:
    """Heuristic pre-render check. Returns a list of (stanza, reason) warnings.

    Uses the actual font metrics so word-wrap matches the real renderer, but
    skips image compositing — fast enough to run over all stanzas before
    piping starts.
    """
    warnings: list[tuple[Stanza, str]] = []
    try:
        font = ImageFont.truetype(str(FONT_REGULAR), font_size)
    except OSError:
        return warnings  # can't check without the font

    line_bbox = font.getbbox("Ag")
    line_height = int((line_bbox[3] - line_bbox[1]) * 1.55)
    max_text_width = width - 2 * margin

    for stanza in stanzas:
        lines = wrap_lines(stanza.text, font, max_text_width)
        total_h = line_height * len(lines)

        # Height overflow
        if total_h > height:
            warnings.append(
                (
                    stanza,
                    f"text block {total_h}px tall exceeds frame height {height}px"
                    f" ({len(lines)} lines × {line_height}px)",
                )
            )

        # Any individual line wider than the text area (shouldn't wrap but catch edge cases)
        for line in lines:
            bbox = font.getbbox(line)
            lw = bbox[2] - bbox[0]
            if lw > max_text_width:
                warnings.append(
                    (
                        stanza,
                        f"line {lw}px wide exceeds text area {max_text_width}px: {line!r}",
                    )
                )
                break  # one warning per stanza is enough

    return warnings


def check_frame_overflow(img: Image.Image, margin: int) -> str | None:
    """Check a rendered RGBA frame for non-transparent pixels outside the safe zone.

    Returns a human-readable message if overflow is detected, else None.
    The safe zone is the frame inset by `margin` on all four sides.
    """
    bbox = img.getbbox()  # bounding box of non-zero pixels across all channels
    if bbox is None:
        return None
    x0, y0, x1, y1 = bbox
    w, h = img.size
    issues = []
    if x0 < margin:
        issues.append(f"left edge ({x0}px < margin {margin}px)")
    if x1 > w - margin:
        issues.append(f"right edge ({x1}px > {w - margin}px)")
    if y0 < margin:
        issues.append(f"top edge ({y0}px < margin {margin}px)")
    if y1 > h - margin:
        issues.append(f"bottom edge ({y1}px > {h - margin}px)")
    return ", ".join(issues) if issues else None


def render_stanza_frame(
    stanza: Stanza,
    width: int,
    height: int,
    font_size: int,
    margin: int,
    color_rgba: tuple[int, int, int, int],
    shadow: bool = False,
    shadow_blur: Sequence[int] = (18,),
    shadow_color_rgba: tuple[int, int, int, int] = (0, 0, 0, 255),
    check_overflow: bool = False,
) -> Image.Image:
    """Render a single stanza onto a transparent RGBA image at full opacity.

    The returned image always has alpha=255 for visible pixels.  Callers that
    need a faded version should use :func:`scale_alpha` rather than re-calling
    this function.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    try:
        font = ImageFont.truetype(str(FONT_REGULAR), font_size)
    except OSError:
        font = ImageFont.load_default()

    max_text_width = width - 2 * margin
    lines = wrap_lines(stanza.text, font, max_text_width)

    # Measure total block height
    line_bbox = font.getbbox("Ag")
    line_height = int((line_bbox[3] - line_bbox[1]) * 1.55)
    total_height = line_height * len(lines)

    start_y = (height - total_height) // 2
    text_color = color_rgba  # always full alpha; fading is done by scale_alpha()

    if shadow:
        shadow_color = shadow_color_rgba
        # Render the text shape once, then composite one blurred layer per radius
        text_shape = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(text_shape)
        for i, line in enumerate(lines):
            bbox = font.getbbox(line)
            line_w = bbox[2] - bbox[0]
            x = (width - line_w) // 2
            y = start_y + i * line_height
            sdraw.text((x, y), line, font=font, fill=shadow_color)
        for radius in shadow_blur:
            if radius > 0:
                img = Image.alpha_composite(
                    img, text_shape.filter(ImageFilter.GaussianBlur(radius=radius))
                )

    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        x = (width - line_w) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font, fill=text_color)

    if check_overflow:
        issue = check_frame_overflow(img, margin)
        if issue:
            print(
                f"\n  Warning: text overflow in stanza [{stanza.section_id}]"
                f" {stanza.text[:40]!r}: {issue}",
                file=sys.stderr,
            )

    return img


def scale_alpha(img: Image.Image, factor: float) -> Image.Image:
    """Return a copy of *img* with its alpha channel scaled by *factor* (0.0–1.0).

    This is used to produce fade frames from a single fully-rendered image,
    avoiding redundant font loading and text layout on every fade step.
    """
    r, g, b, a = img.split()
    a = a.point(lambda px: int(px * factor))
    return Image.merge("RGBA", (r, g, b, a))


def stanza_hold_frames(
    stanza: Stanza, hold_secs: float, fps: int, auto_timing: bool
) -> int:
    """Return the hold frame count for a stanza.

    With auto_timing: hold_secs is seconds for the first line; additional lines
    are discounted by a sqrt curve — each line adds less time than the last.
    A 1-line stanza holds for hold_secs; a 4-line stanza holds for 2× hold_secs
    (not 4×), matching the sublinear nature of reading multi-line text.

    Without auto_timing: fixed hold_secs for every stanza.
    """
    if auto_timing:
        n_lines = max(1, len(stanza.lines))
        return max(1, int(hold_secs * math.sqrt(n_lines) * fps))
    return max(1, int(hold_secs * fps))


def iter_frames(
    stanzas: list[Stanza],
    width: int,
    height: int,
    fps: int,
    hold_secs: float,
    fade_secs: float,
    gap_secs: float,
    font_size: int,
    margin: int,
    color_hex: str,
    shadow: bool,
    title_hold_secs: float = 4.0,
    title_fade_secs: float = 1.5,
    logo_scale: float = 0.22,
    auto_timing: bool = False,
    shadow_blur: Sequence[int] = (18,),
    shadow_color_rgba: tuple[int, int, int, int] = (0, 0, 0, 255),
    tail_frames: int = 0,
) -> Generator[Image.Image, None, None]:
    """Yield RGBA overlay frames one at a time — no disk I/O."""
    color_rgba = hex_to_rgba(color_hex)
    fade_frames = max(1, int(fade_secs * fps))
    gap_frames = max(0, int(gap_secs * fps))
    title_fade_frames = max(1, int(title_fade_secs * fps))
    title_hold_frames = max(1, int(title_hold_secs * fps))

    blank = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # ------------------------------------------------------------------
    # Title card
    # ------------------------------------------------------------------
    print("  Rendering title card…", flush=True)

    # Pre-build the tinted logo once to avoid reloading it on every fade frame.
    color_rgb = (color_rgba[0], color_rgba[1], color_rgba[2])
    logo_h = int(height * logo_scale)
    prebuilt_logo: Image.Image | None = None
    if LOGO_PNG.exists():
        prebuilt_logo = tint_logo(LOGO_PNG, color_rgb, logo_h)

    def _title_frame(al: float, aw: float) -> Image.Image:
        return render_title_card(
            width,
            height,
            color_rgba,
            logo_scale,
            al,
            aw,
            shadow,
            _prebuilt_logo=prebuilt_logo,
        )

    for f in range(title_fade_frames):
        yield _title_frame(f / title_fade_frames, 0.0)
    for f in range(title_fade_frames):
        yield _title_frame(1.0, f / title_fade_frames)

    img_full = _title_frame(1.0, 1.0)
    for _ in range(title_hold_frames):
        yield img_full

    for f in range(title_fade_frames):
        a = 1.0 - (f + 1) / title_fade_frames
        yield _title_frame(a, a)

    for _ in range(gap_frames):
        yield blank

    # ------------------------------------------------------------------
    # Stanzas
    # ------------------------------------------------------------------
    total = len(stanzas)
    for n, stanza in enumerate(stanzas):
        print(
            f"\r  Stanza {n + 1}/{total} ({(n + 1) / total:.0%})…", end="", flush=True
        )

        # Render once at full opacity; derive faded frames via alpha scaling.
        img_full = render_stanza_frame(
            stanza,
            width,
            height,
            font_size,
            margin,
            color_rgba,
            shadow,
            shadow_blur,
            shadow_color_rgba,
            check_overflow=True,
        )

        for f in range(fade_frames):
            yield scale_alpha(img_full, f / fade_frames)

        for _ in range(stanza_hold_frames(stanza, hold_secs, fps, auto_timing)):
            yield img_full

        for f in range(fade_frames):
            yield scale_alpha(img_full, 1.0 - (f + 1) / fade_frames)

        for _ in range(gap_frames):
            yield blank

    print()

    # Seamless loop tail — transparent frames so the bg plays to its loop point
    if tail_frames > 0:
        print(
            f"  Appending {tail_frames} tail frames ({tail_frames / fps:.1f}s) for seamless loop…"
        )
        for _ in range(tail_frames):
            yield blank


def count_frames(
    stanzas: list[Stanza],
    fps: int,
    hold_secs: float,
    fade_secs: float,
    gap_secs: float,
    title_hold_secs: float,
    title_fade_secs: float,
    auto_timing: bool = False,
    tail_frames: int = 0,
) -> int:
    """Return total frame count without rendering anything."""
    fade = max(1, int(fade_secs * fps))
    gap = max(0, int(gap_secs * fps))
    t_fade = max(1, int(title_fade_secs * fps))
    t_hold = max(1, int(title_hold_secs * fps))
    title = 3 * t_fade + t_hold + gap
    stanza_total = sum(
        fade * 2 + stanza_hold_frames(s, hold_secs, fps, auto_timing) + gap
        for s in stanzas
    )
    return title + stanza_total + tail_frames


# ---------------------------------------------------------------------------
# --frames-only helper (debug / Kdenlive import)
# ---------------------------------------------------------------------------


def write_frames_to_dir(frames: Iterable[Image.Image], out_dir: Path) -> int:
    """Save each frame as a numbered PNG. Returns frame count."""
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for count, img in enumerate(frames, start=1):
        img.save(out_dir / f"frame_{count:07d}.png")
    return count


# ---------------------------------------------------------------------------
# FFmpeg compositing
# ---------------------------------------------------------------------------


def probe_video_size(path: Path) -> tuple[int, int]:
    """Return (width, height) of the first video stream in path via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"ffprobe failed on {path}: {result.stderr.strip()}")
    first_line = result.stdout.strip().splitlines()[0]
    w, h = first_line.split(",")
    return int(w), int(h)


def probe_video_duration(path: Path) -> float:
    """Return duration in seconds of the video at path via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"ffprobe failed on {path}: {result.stderr.strip()}")
    return float(result.stdout.strip())


def _highlight_rolloff_curve(amount: float) -> str:
    """Return an FFmpeg curves filter string that compresses highlights.

    amount=0.0 → identity (no change)
    amount=1.0 → heavy highlight rolloff: top pulled to 0.60, mids barely touched

    The curve is defined by four control points interpolated between identity
    and the full-rolloff target:

        input  → output (at amount=1.0)
        0.00   → 0.00   (blacks stay black)
        0.30   → 0.29   (low-mids almost untouched)
        0.70   → 0.51   (upper-mids pulled proportionally)
        1.00   → 0.60   (highlights capped at 60 %)

    At intermediate amounts each output value is linearly interpolated between
    identity and the target.
    """
    # (input, target_output_at_amount_1)
    points = [(0.0, 0.0), (0.30, 0.29), (0.70, 0.51), (1.0, 0.60)]
    pts = []
    for x, y_target in points:
        y = x + (y_target - x) * amount  # lerp between identity and target
        pts.append(f"{x:.4f}/{y:.4f}")
    return "curves=all='" + " ".join(pts) + "'"


def composite_with_ffmpeg(
    bg_path: Path,
    frames: Generator[Image.Image, None, None],
    total_frames: int,
    fps: int,
    out_path: Path,
    out_width: int,
    out_height: int,
    darken: float = 0.0,
):
    """Composite overlay frames (streamed via stdin) over the looped background.

    Frames are sent as raw RGBA bytes — no temp files written.
    """
    duration = total_frames / fps

    try:
        bg_w, bg_h = probe_video_size(bg_path)
        needs_pad = bg_w != out_width or bg_h != out_height
        if needs_pad:
            print(
                f"  Background is {bg_w}×{bg_h}, output is {out_width}×{out_height} — padding with black."
            )
    except RuntimeError as e:
        print(
            f"  Warning: could not probe background size ({e}). Assuming no padding needed."
        )
        needs_pad = False

    curve_filter = f",{_highlight_rolloff_curve(darken)}" if darken > 0.0 else ""

    if needs_pad:
        bg_filter = (
            f"[0:v]trim=duration={duration:.3f},setpts=PTS-STARTPTS,"
            f"scale={out_width}:{out_height}:force_original_aspect_ratio=decrease,"
            f"pad={out_width}:{out_height}:(ow-iw)/2:(oh-ih)/2:black"
            f"{curve_filter}[bg]"
        )
    else:
        bg_filter = (
            f"[0:v]trim=duration={duration:.3f},setpts=PTS-STARTPTS{curve_filter}[bg]"
        )

    cmd = [
        "ffmpeg",
        "-y",
        # Background video (looped)
        "-stream_loop",
        "-1",
        "-i",
        str(bg_path),
        # Overlay: raw RGBA frames from stdin
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgba",
        "-s",
        f"{out_width}x{out_height}",
        "-r",
        str(fps),
        "-i",
        "pipe:0",
        "-filter_complex",
        bg_filter + ";"
        "[1:v]setpts=PTS-STARTPTS[txt];"
        "[bg][txt]overlay=format=auto,format=yuv420p[out]",
        "-map",
        "[out]",
        "-t",
        f"{duration:.3f}",
        "-c:v",
        "libx265",
        "-crf",
        "22",
        "-preset",
        "slow",
        "-tag:v",
        "hvc1",
        str(out_path),
    ]

    print("Running FFmpeg…")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        for img in frames:
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
    except BrokenPipeError:
        stderr_out = proc.stderr.read().decode(errors="replace")
        proc.wait()
        print("FFmpeg pipe closed early.", file=sys.stderr)
        if stderr_out.strip():
            print(stderr_out, file=sys.stderr)
        sys.exit(1)

    stderr_out = proc.stderr.read().decode(errors="replace")
    proc.wait()
    if proc.returncode != 0:
        print("FFmpeg failed.", file=sys.stderr)
        if stderr_out.strip():
            print(stderr_out, file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Render Covenant ritual text over a background video.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars="@",
        epilog=__doc__,
    )
    p.add_argument(
        "--bg",
        metavar="PATH",
        help="Background video to loop (required unless --frames-only)",
    )
    p.add_argument(
        "--out",
        metavar="PATH",
        default=str(DIST_DIR / "covenant_ritual.mp4"),
        help="Output video path",
    )
    p.add_argument(
        "--ritual", metavar="PATH", default=str(RITUAL_MD), help="Ritual markdown file"
    )
    p.add_argument("--fps", type=int, default=30)
    p.add_argument(
        "--hold", type=float, default=5.0, metavar="SECS", help="Hold time per stanza"
    )
    p.add_argument(
        "--fade", type=float, default=1.5, metavar="SECS", help="Fade in/out duration"
    )
    p.add_argument(
        "--gap",
        type=float,
        default=0.5,
        metavar="SECS",
        help="Silent gap between stanzas",
    )
    p.add_argument(
        "--title-hold",
        type=float,
        default=4.0,
        metavar="SECS",
        help="Seconds the title card is fully visible",
    )
    p.add_argument(
        "--title-fade",
        type=float,
        default=1.5,
        metavar="SECS",
        help="Fade duration for title card elements",
    )
    p.add_argument(
        "--logo-scale",
        type=float,
        default=0.44,
        metavar="FRAC",
        help="Logo height as fraction of frame height",
    )
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--font-size", type=int, default=72, metavar="PT")
    p.add_argument(
        "--margin", type=int, default=120, metavar="PX", help="Horizontal text margin"
    )
    p.add_argument("--color", default="#f5f0e8", metavar="HEX", help="Text colour")
    p.add_argument("--shadow", action="store_true", help="Add centred glow shadow")
    p.add_argument(
        "--shadow-blur",
        default="18",
        metavar="PX[,PX...]",
        help="Comma-separated blur radii to stack additively (e.g. 3,12); default 18",
    )
    p.add_argument(
        "--shadow-color",
        default="000000FF",
        metavar="HEX",
        help="Shadow colour as hex RGB or RGBA: #000000, 000000, or 000000FF (default 000000FF)",
    )
    p.add_argument(
        "--darken",
        type=float,
        default=0.0,
        metavar="AMOUNT",
        help="Highlight rolloff 0–1: compresses bright pixels while leaving shadows alone (0=off, 1=heavy)",
    )
    p.add_argument(
        "--sections", metavar="ID,ID,...", help="Comma-separated section IDs to include"
    )
    p.add_argument(
        "--list-sections",
        action="store_true",
        help="List available section IDs and exit",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Run layout check only — print all stanzas that overflow and exit (no rendering)",
    )
    p.add_argument(
        "--seamless-loop",
        action="store_true",
        help="Extend output so total duration is a multiple of the background video duration",
    )
    p.add_argument(
        "--frames-only",
        metavar="DIR",
        help="Write PNG frames to DIR and exit (skip FFmpeg)",
    )
    p.add_argument(
        "--preview",
        type=float,
        default=None,
        metavar="SECS",
        help="Render only the first N seconds (title card + as many stanzas as fit)",
    )
    p.add_argument(
        "--auto-timing",
        action="store_true",
        help="Scale hold time with stanza line count (--hold becomes seconds-per-line)",
    )
    return p


def main():
    p = build_parser()
    args = p.parse_args()
    shadow_blur_list = [
        int(v.strip()) for v in args.shadow_blur.split(",") if v.strip()
    ]

    # --- Input validation ---
    if args.fps <= 0:
        p.error("--fps must be > 0")
    if args.font_size <= 0:
        p.error("--font-size must be > 0")
    if args.logo_scale <= 0:
        p.error("--logo-scale must be > 0")
    if not 0.0 <= args.darken <= 1.0:
        p.error("--darken must be between 0.0 and 1.0")

    ritual_path = Path(args.ritual)
    if not ritual_path.exists():
        print(f"Error: ritual file not found: {ritual_path}", file=sys.stderr)
        print(
            "Run `make compose` first to generate dist/covenant.ritual.md",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Parsing {ritual_path} …")
    all_stanzas = parse_ritual(ritual_path)

    if args.list_sections:
        seen: dict[str, str] = {}
        for s in all_stanzas:
            if s.section_id not in seen:
                seen[s.section_id] = s.section_title
        print(f"{'ID':<45} Title")
        print("-" * 70)
        for sid, title in seen.items():
            print(f"{sid:<45} {title}")
        return

    # Filter sections
    if args.sections:
        wanted = {sid.strip() for sid in args.sections.split(",")}
        stanzas = [s for s in all_stanzas if s.section_id in wanted]
        if not stanzas:
            print(f"No stanzas found for sections: {args.sections}", file=sys.stderr)
            sys.exit(1)
        print(f"Filtered to {len(stanzas)} stanzas from {len(wanted)} section(s).")
    else:
        stanzas = all_stanzas
        print(f"Found {len(stanzas)} stanzas across all sections.")

    # Estimate duration — use count_frames so --auto-timing is accounted for
    title_secs = (
        args.title_hold + 2 * args.title_fade + args.gap
    )  # used for preview budget
    stanza_secs = (
        args.hold + 2 * args.fade + args.gap
    )  # used for preview budget (approx)

    # Preview truncation — trim stanza list so total duration fits within limit
    if args.preview is not None:
        budget = args.preview - title_secs
        max_stanzas = max(0, int(budget // stanza_secs))
        if max_stanzas < len(stanzas):
            print(
                f"--preview {args.preview}s: using {max_stanzas} of {len(stanzas)} stanzas."
            )
            stanzas = stanzas[:max_stanzas]

    total_frames_est = count_frames(
        stanzas,
        args.fps,
        args.hold,
        args.fade,
        args.gap,
        args.title_hold,
        args.title_fade,
        auto_timing=args.auto_timing,
    )
    total_secs = total_frames_est / args.fps
    mins, secs = divmod(int(total_secs), 60)
    print(f"Estimated duration: {mins}m {secs}s  ({len(stanzas)} stanzas + title)")

    # --- Heuristic pre-render fit check ---
    fit_warnings = check_stanzas_fit(
        stanzas, args.width, args.height, args.font_size, args.margin
    )
    if fit_warnings:
        print(
            f"  Warning: {len(fit_warnings)} stanza(s) may not fit at font-size {args.font_size}:",
            file=sys.stderr,
        )
        for stanza, reason in fit_warnings:
            print(
                f"    [{stanza.section_id}] {stanza.text[:50]!r} — {reason}",
                file=sys.stderr,
            )
    else:
        print(
            f"  Layout check: all {len(stanzas)} stanzas fit within {args.width}×{args.height} at font-size {args.font_size}."
        )

    if args.dry_run:
        # Seamless loop tail estimate (informational only)
        if args.seamless_loop:
            if args.bg:
                bg_path_dry = Path(args.bg)
                if bg_path_dry.exists():
                    try:
                        bg_duration = probe_video_duration(bg_path_dry)
                        content_frames = count_frames(
                            stanzas,
                            args.fps,
                            args.hold,
                            args.fade,
                            args.gap,
                            args.title_hold,
                            args.title_fade,
                            auto_timing=args.auto_timing,
                        )
                        content_secs = content_frames / args.fps
                        loops = math.ceil(content_secs / bg_duration)
                        target_secs = loops * bg_duration
                        tail_frames_dry = round((target_secs - content_secs) * args.fps)
                        print(
                            f"  Seamless loop: bg is {bg_duration:.2f}s, "
                            f"content is {content_secs:.1f}s, "
                            f"padding {tail_frames_dry / args.fps:.1f}s tail to reach {loops}× loop ({target_secs:.2f}s)."
                        )
                    except RuntimeError as e:
                        print(
                            f"  Warning: could not probe bg for seamless loop estimate ({e})."
                        )
                else:
                    print(
                        f"  Warning: --bg path not found, skipping seamless loop estimate."
                    )
            else:
                print("  Note: pass --bg to see seamless loop tail estimate.")

        if fit_warnings:
            print(f"\n--- DRY RUN: {len(fit_warnings)} overflowing stanza(s) ---\n")
            for stanza, reason in fit_warnings:
                print(f"[{stanza.section_id}] {reason}")
                print(stanza.text)
                print()
        else:
            print(f"\nDRY RUN: all {len(stanzas)} stanzas fit. No issues.")
        return

    if args.frames_only:
        frames_dir = Path(args.frames_only)
        print(f"Writing frames to {frames_dir} …")
        frames = iter_frames(
            stanzas,
            args.width,
            args.height,
            args.fps,
            args.hold,
            args.fade,
            args.gap,
            args.font_size,
            args.margin,
            args.color,
            args.shadow,
            title_hold_secs=args.title_hold,
            title_fade_secs=args.title_fade,
            logo_scale=args.logo_scale,
            auto_timing=args.auto_timing,
            shadow_blur=shadow_blur_list,
            shadow_color_rgba=hex_to_rgba(args.shadow_color),
        )
        n = write_frames_to_dir(frames, frames_dir)
        print(f"Done. {n} frames written to {frames_dir}")
        return

    if not args.bg:
        print(
            "Error: --bg <background_video> is required (or use --frames-only).",
            file=sys.stderr,
        )
        sys.exit(1)

    bg_path = Path(args.bg)
    if not bg_path.exists():
        print(f"Error: background video not found: {bg_path}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Seamless loop tail — pad to next multiple of bg video duration
    tail_frames = 0
    if args.seamless_loop:
        try:
            bg_duration = probe_video_duration(bg_path)
            content_frames = count_frames(
                stanzas,
                args.fps,
                args.hold,
                args.fade,
                args.gap,
                args.title_hold,
                args.title_fade,
                auto_timing=args.auto_timing,
            )
            content_secs = content_frames / args.fps
            loops = math.ceil(content_secs / bg_duration)
            target_secs = loops * bg_duration
            tail_frames = round((target_secs - content_secs) * args.fps)
            print(
                f"  Seamless loop: bg is {bg_duration:.2f}s, "
                f"content is {content_secs:.1f}s, "
                f"padding {tail_frames / args.fps:.1f}s tail to reach {loops}× loop ({target_secs:.2f}s)."
            )
        except RuntimeError as e:
            print(
                f"  Warning: could not probe bg duration for seamless loop ({e}). Skipping tail."
            )

    total_frames = count_frames(
        stanzas,
        args.fps,
        args.hold,
        args.fade,
        args.gap,
        args.title_hold,
        args.title_fade,
        auto_timing=args.auto_timing,
        tail_frames=tail_frames,
    )
    print(f"Total frames to pipe: {total_frames}")

    frames = iter_frames(
        stanzas,
        args.width,
        args.height,
        args.fps,
        args.hold,
        args.fade,
        args.gap,
        args.font_size,
        args.margin,
        args.color,
        args.shadow,
        title_hold_secs=args.title_hold,
        title_fade_secs=args.title_fade,
        logo_scale=args.logo_scale,
        auto_timing=args.auto_timing,
        shadow_blur=shadow_blur_list,
        shadow_color_rgba=hex_to_rgba(args.shadow_color),
        tail_frames=tail_frames,
    )
    composite_with_ffmpeg(
        bg_path,
        frames,
        total_frames,
        args.fps,
        out_path,
        args.width,
        args.height,
        darken=args.darken,
    )

    print(f"\nOutput written to: {out_path}")


if __name__ == "__main__":
    main()
