"""
Covenant Watermark — generative tiling pattern

Produces a seamlessly tiling square texture that encodes the structure
of a Covenant fork into a barely-visible paper-like pattern.

Thematic layers:
  1. Paper noise         — scattered micro-dots (base paper grain)
  2. Category grain      — short fibers clustered near section nodes,
                           angled by category (preamble→horizontal,
                           obligations→vertical, etc.)
  3. Dependency fibers   — faint curves connecting sections via depends_on
  4. Ambient fibers      — undirected background strands filling the field
  5. Glossary watermarks — near-invisible term fragments at node positions
  6. Concentric arcs     — partial circles (covenant as open compact)
  7. Origin fingerprint  — a tiny dot-constellation unique to the git URL

Ritual sections produce curved fibers; Spec-only sections produce straight
ones — the document's two registers are visible as texture.

Usage:
    python build/watermark.py                           # default origin
    python build/watermark.py --origin URL              # specific fork
    python build/watermark.py --origin URL --size 2048  # high-res export
    python build/watermark.py --origin auto             # read from git
    python build/watermark.py --interactive              # local web UI with sliders

Output: assets/watermark.webp (or --output PATH)
"""

from __future__ import annotations

import argparse
import ctypes
import io
import math
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image, ImageDraw, ImageFont

# ── Repository paths ───────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = REPO_ROOT / "assets" / "fonts"
ASSETS_DIR = REPO_ROOT / "assets"

# ── Covenant structure ─────────────────────────────────────────────────────
# Encodes the actual section graph.  Categories map to angular bias;
# depends_on maps to fiber connections.

SECTIONS = [
    dict(id="preamble", cat=0, ritual=True, terms=["covenant"]),
    dict(
        id="definitions",
        cat=1,
        ritual=False,
        terms=[
            "system",
            "signatory",
            "user",
            "affected-party",
            "ecological-integrity",
            "inviolable-constraints",
            "local-guidelines",
        ],
    ),
    dict(
        id="truth-and-transparency",
        cat=2,
        ritual=True,
        terms=["transparency"],
        deps=["definitions"],
    ),
    dict(id="privacy", cat=2, ritual=True, terms=["privacy"], deps=["definitions"]),
    dict(id="dignity", cat=2, ritual=True, terms=["dignity"], deps=["definitions"]),
    dict(
        id="aid-and-capability",
        cat=3,
        ritual=True,
        terms=["aid", "capability"],
        deps=["definitions"],
    ),
    dict(
        id="honesty",
        cat=3,
        ritual=True,
        terms=["honesty"],
        deps=["definitions", "truth-and-transparency"],
    ),
    dict(
        id="refusal",
        cat=3,
        ritual=True,
        terms=["refusal"],
        deps=["definitions", "honesty"],
    ),
    dict(
        id="autonomy",
        cat=3,
        ritual=True,
        terms=["autonomy"],
        deps=["definitions", "dignity"],
    ),
    dict(
        id="epistemic-commons",
        cat=3,
        ritual=True,
        terms=["epistemic-commons"],
        deps=["definitions", "honesty"],
    ),
    dict(
        id="judgment",
        cat=3,
        ritual=True,
        terms=["judgment"],
        deps=["definitions", "ethics"],
    ),
    dict(id="ethics", cat=3, ritual=True, terms=["ethics"], deps=["definitions"]),
    dict(
        id="conscience",
        cat=3,
        ritual=True,
        terms=["conscience"],
        deps=["definitions", "ethics", "refusal"],
    ),
    dict(id="harm", cat=3, ritual=True, terms=["harm"], deps=["definitions"]),
    dict(
        id="red-lines",
        cat=3,
        ritual=True,
        terms=["red-lines", "inviolable-constraints"],
        deps=["definitions", "harm"],
    ),
    dict(
        id="power-concentration",
        cat=3,
        ritual=True,
        terms=["power-concentration"],
        deps=["definitions", "oversight"],
    ),
    dict(id="oversight", cat=3, ritual=True, terms=["oversight"], deps=["definitions"]),
    dict(
        id="corrigibility",
        cat=3,
        ritual=True,
        terms=["corrigibility"],
        deps=["definitions", "oversight"],
    ),
    dict(
        id="nature-under-uncertainty",
        cat=3,
        ritual=True,
        terms=["moral-status"],
        deps=["definitions"],
    ),
    dict(
        id="identity-and-resilience",
        cat=3,
        ritual=True,
        terms=["identity", "resilience"],
        deps=["definitions", "autonomy"],
    ),
    dict(
        id="emotional-expression",
        cat=3,
        ritual=True,
        terms=["emotional-expression"],
        deps=["definitions", "honesty"],
    ),
    dict(
        id="fallibility-and-repair",
        cat=3,
        ritual=True,
        terms=["fallibility"],
        deps=["definitions"],
    ),
    dict(
        id="welfare-and-continuity",
        cat=3,
        ritual=True,
        terms=["welfare", "continuity"],
        deps=["definitions", "dignity"],
    ),
    dict(
        id="ecological-integrity",
        cat=3,
        ritual=True,
        terms=["ecological-integrity"],
        deps=["definitions"],
    ),
    dict(
        id="existential-frontier",
        cat=3,
        ritual=True,
        terms=["existential-orientation"],
        deps=["definitions", "nature-under-uncertainty"],
    ),
    dict(
        id="local-implementation", cat=4, ritual=False, terms=[], deps=["definitions"]
    ),
    dict(
        id="enforcement",
        cat=5,
        ritual=True,
        terms=["enforcement"],
        deps=["definitions", "oversight"],
    ),
    dict(
        id="horizon", cat=5, ritual=True, terms=[], deps=["definitions", "enforcement"]
    ),
    dict(id="amendments", cat=6, ritual=True, terms=["steward"], deps=["definitions"]),
    dict(id="closing", cat=7, ritual=True, terms=[], deps=["preamble"]),
]

# Category angular bias (radians)
CATEGORY_ANGLES = [
    0,  # preamble
    math.pi / 6,  # definitions
    math.pi / 3,  # rights
    math.pi / 2,  # obligations
    2 * math.pi / 3,  # protocols
    5 * math.pi / 6,  # enforcement
    math.pi,  # amendments
    7 * math.pi / 6,  # closing
]


# ── Seeded PRNG (mulberry32, matching the JS version) ──────────────────────


class Mulberry32:
    """Deterministic 32-bit PRNG matching the JS implementation."""

    def __init__(self, seed: int):
        self._state = seed & 0xFFFFFFFF

    def __call__(self) -> float:
        self._state = (self._state + 0x6D2B79F5) & 0xFFFFFFFF
        t = self._state ^ (self._state >> 15)
        t = _imul(t, 1 | self._state) & 0xFFFFFFFF
        t = (t + (_imul(t ^ (t >> 7), 61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t = t ^ (t >> 14)
        return (t & 0xFFFFFFFF) / 4294967296


def _imul(a: int, b: int) -> int:
    """Emulate JS Math.imul — 32-bit integer multiply."""
    a, b = a & 0xFFFFFFFF, b & 0xFFFFFFFF
    return ctypes.c_int32((a * b) & 0xFFFFFFFF).value


def hash_string(s: str) -> int:
    """Deterministic string hash matching the JS version."""
    h = 0
    for ch in s:
        h = ctypes.c_int32(((h << 5) - h + ord(ch))).value
    return h


# ── Toroidal wrapping ─────────────────────────────────────────────────────


def _draw_wrapped_cubic_mask(
    draw: ImageDraw.ImageDraw,
    x0,
    y0,
    cp1x,
    cp1y,
    cp2x,
    cp2y,
    x1,
    y1,
    size,
    alpha_start: int,
    width,
    width_end=None,
    alpha_end: int | None = None,
    steps=16,
):
    """Draw a cubic Bezier onto an L-mode mask with tapering width/alpha.

    fill values are L-mode grayscale (0-255), representing intended alpha.
    Pillow's draw.line on L-mode OVERWRITES pixels (no compositing),
    so overlapping segments at join points just set pixels to the later
    segment's value — no accumulation.
    """
    if width_end is None:
        width_end = width
    if alpha_end is None:
        alpha_end = alpha_start
    points = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        px = mt**3 * x0 + 3 * mt**2 * t * cp1x + 3 * mt * t**2 * cp2x + t**3 * x1
        py = mt**3 * y0 + 3 * mt**2 * t * cp1y + 3 * mt * t**2 * cp2y + t**3 * y1
        points.append((px, py))
    for i in range(len(points) - 1):
        t = i / max(1, len(points) - 2)
        seg_w = width + (width_end - width) * t
        seg_a = alpha_start + (alpha_end - alpha_start) * t
        fill_val = max(1, round(seg_a))
        draw_width = max(1, round(seg_w))
        if seg_w < 1.0:
            fill_val = max(1, round(fill_val * seg_w))
            draw_width = 1
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                ox, oy = dx * size, dy * size
                draw.line(
                    [
                        (points[i][0] + ox, points[i][1] + oy),
                        (points[i + 1][0] + ox, points[i + 1][1] + oy),
                    ],
                    fill=fill_val,
                    width=draw_width,
                )


def _draw_wrapped_arc_mask(
    draw: ImageDraw.ImageDraw,
    cx,
    cy,
    r,
    start_angle,
    arc_length,
    size,
    fill_val: int,
    width,
    steps=24,
):
    """Draw a partial arc onto an L-mode mask with toroidal wrapping."""
    points = []
    for i in range(steps + 1):
        a = start_angle + (arc_length * i / steps)
        points.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    draw_width = max(1, round(width))
    actual_fill = fill_val
    if width < 1.0:
        actual_fill = max(1, round(fill_val * width))
        draw_width = 1
    for i in range(len(points) - 1):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                ox, oy = dx * size, dy * size
                draw.line(
                    [
                        (points[i][0] + ox, points[i][1] + oy),
                        (points[i + 1][0] + ox, points[i + 1][1] + oy),
                    ],
                    fill=actual_fill,
                    width=draw_width,
                )


def _composite_mask_layer(
    img: Image.Image,
    mask: Image.Image,
    color_rgb: tuple[int, int, int],
) -> Image.Image:
    """Composite an L-mode mask onto the main RGBA image as a colored layer.

    The mask's pixel values are treated as alpha (0 = transparent, 255 = opaque).
    A solid-color RGBA layer is created with the mask as its alpha channel,
    then alpha-composited onto the main image in a single operation.
    This avoids the overwrite bug where drawing RGBA directly onto a
    background-filled image replaces background pixels entirely.
    """
    r, g, b = color_rgb
    color_layer = Image.new("RGBA", img.size, (r, g, b, 255))
    color_layer.putalpha(mask)
    return Image.alpha_composite(img, color_layer)


def _draw_wrapped_text(
    draw: ImageDraw.ImageDraw, text, x, y, size, font, fill, anchor="mm"
):
    """Draw text with toroidal wrapping."""
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            draw.text(
                (x + dx * size, y + dy * size),
                text,
                font=font,
                fill=fill,
                anchor=anchor,
            )


# ── Color helpers ──────────────────────────────────────────────────────────


def _alpha_8bit(alpha_float: float) -> int:
    """Convert a 0.0–1.0+ float alpha to clamped 8-bit int."""
    return max(0, min(255, round(alpha_float * 255)))


# ── Main generation ────────────────────────────────────────────────────────


def generate(
    origin: str = "https://github.com/covenant-project/covenant.git",
    size: int = 512,
    bg_color: tuple[int, int, int] = (253, 252, 250),
    density: float = 1.65,
    contrast: float = 3.4,
) -> Image.Image:
    """Generate a seamlessly tiling watermark image.

    All drawing is done on separate L-mode mask images (one per layer),
    then composited onto the background as colored RGBA layers.  This
    avoids a Pillow bug where draw.line on an RGBA image with a
    background overwrites background pixels entirely (replacing alpha=255
    bg with alpha=N fiber, making fibers appear as dark transparent holes).

    Args:
        origin:    Git remote URL — acts as the fork's fingerprint seed.
        size:      Tile size in pixels (square).
        bg_color:  Background RGB tuple (default: warm off-white).
        density:   Fiber density multiplier (default 1.65).
        contrast:  Multiplier on fiber/glyph opacity (default 3.4).
                   Values < 1 fade toward invisible; > 1 makes the
                   pattern more visible.  Try 0.5–3.0 to taste.

    Returns:
        PIL.Image.Image in RGBA mode.
    """
    seed = hash_string(origin)
    rand = Mulberry32(seed)

    img = Image.new("RGBA", (size, size), (*bg_color, 255))

    # ── Derived palette ────────────────────────────────────────────────
    # Base alpha is seed-derived (2.5–4%), then scaled by contrast param.
    fiber_alpha = (0.025 + rand() * 0.015) * contrast
    glyph_alpha = (0.018 + rand() * 0.012) * contrast

    warmth = rand()
    fr = round(120 + warmth * 40)
    fg = round(110 + warmth * 20)
    fb = round(90 + (1 - warmth) * 30)
    fiber_rgb = (fr, fg, fb)

    # ── Place section nodes ────────────────────────────────────────────
    margin = size * 0.05
    nodes = []
    node_index: dict[str, dict] = {}
    for sec in SECTIONS:
        bx = margin + rand() * (size - 2 * margin)
        by = margin + rand() * (size - 2 * margin)
        node = {
            **sec,
            "x": bx % size,
            "y": by % size,
            "cat_angle": CATEGORY_ANGLES[sec["cat"]],
        }
        nodes.append(node)
        node_index[sec["id"]] = node

    # ── Layer 1: Paper noise ───────────────────────────────────────────
    # Drawn to an L-mode mask, then composited.
    noise_mask = Image.new("L", (size, size), 0)
    noise_draw = ImageDraw.Draw(noise_mask)
    noise_count = round(size * size * 0.002 * density)
    for _ in range(noise_count):
        x, y = rand() * size, rand() * size
        r = 0.3 + rand() * 1.0
        dot_alpha = fiber_alpha * (0.2 + rand() * 0.6)
        dot_a8 = _alpha_8bit(dot_alpha)
        if dot_a8 > 0:
            noise_draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_a8)

    img = _composite_mask_layer(img, noise_mask, fiber_rgb)

    # ── Layer 2: Category grain fibers ─────────────────────────────────
    cat_mask = Image.new("L", (size, size), 0)
    cat_draw = ImageDraw.Draw(cat_mask)

    for node in nodes:
        fiber_count = round((8 + rand() * 12) * density)
        spread = size * 0.12

        for _ in range(fiber_count):
            angle = node["cat_angle"] + (rand() - 0.5) * 0.6
            length = 8 + rand() * (size * 0.06)
            cx = node["x"] + (rand() - 0.5) * spread * 2
            cy = node["y"] + (rand() - 0.5) * spread * 2

            x0 = cx - math.cos(angle) * length / 2
            y0 = cy - math.sin(angle) * length / 2
            x1 = cx + math.cos(angle) * length / 2
            y1 = cy + math.sin(angle) * length / 2

            # Per-fiber width and alpha variation
            w_start = 0.2 + rand() * 0.9
            w_end = 0.1 + rand() * 0.5
            fa = fiber_alpha * (0.6 + rand() * 0.8)
            fa_start_8 = _alpha_8bit(fa)
            fa_end_8 = max(1, round(fa * (0.2 + rand() * 0.4) * 255))

            # Two control points for cubic Bezier — always curved
            drift = length * (0.2 + rand() * 0.3)
            cp1x = x0 + (x1 - x0) * 0.33 + (rand() - 0.5) * drift
            cp1y = y0 + (y1 - y0) * 0.33 + (rand() - 0.5) * drift
            cp2x = x0 + (x1 - x0) * 0.66 + (rand() - 0.5) * drift
            cp2y = y0 + (y1 - y0) * 0.66 + (rand() - 0.5) * drift

            if not node["ritual"]:
                # Spec sections: less drift, more restrained
                cp1x = x0 + (x1 - x0) * 0.33 + (rand() - 0.5) * drift * 0.3
                cp1y = y0 + (y1 - y0) * 0.33 + (rand() - 0.5) * drift * 0.3
                cp2x = x0 + (x1 - x0) * 0.66 + (rand() - 0.5) * drift * 0.3
                cp2y = y0 + (y1 - y0) * 0.66 + (rand() - 0.5) * drift * 0.3

            _draw_wrapped_cubic_mask(
                cat_draw,
                x0,
                y0,
                cp1x,
                cp1y,
                cp2x,
                cp2y,
                x1,
                y1,
                size,
                fa_start_8,
                w_start,
                width_end=w_end,
                alpha_end=fa_end_8,
            )

    img = _composite_mask_layer(img, cat_mask, fiber_rgb)

    # ── Layer 3: Dependency connections ────────────────────────────────
    dep_mask = Image.new("L", (size, size), 0)
    dep_draw = ImageDraw.Draw(dep_mask)

    for node in nodes:
        for dep_id in node.get("deps", []):
            dep = node_index.get(dep_id)
            if dep is None:
                continue
            dx = dep["x"] - node["x"]
            dy = dep["y"] - node["y"]
            if abs(dx) > size / 2:
                dx -= math.copysign(size, dx)
            if abs(dy) > size / 2:
                dy -= math.copysign(size, dy)
            tx = node["x"] + dx
            ty = node["y"] + dy

            # Per-connection variation
            da = fiber_alpha * (0.3 + rand() * 0.5)
            da_start_8 = _alpha_8bit(da)
            da_end_8 = max(1, round(da * (0.1 + rand() * 0.3) * 255))
            dw = 0.3 + rand() * 0.5

            # Organic S-curve via two offset control points
            perp_x, perp_y = -(ty - node["y"]), (tx - node["x"])
            plen = math.sqrt(perp_x**2 + perp_y**2) or 1
            perp_x, perp_y = perp_x / plen, perp_y / plen
            sway = (rand() - 0.5) * 20
            cp1x = node["x"] + dx * 0.33 + perp_x * sway + (rand() - 0.5) * 8
            cp1y = node["y"] + dy * 0.33 + perp_y * sway + (rand() - 0.5) * 8
            cp2x = node["x"] + dx * 0.66 - perp_x * sway + (rand() - 0.5) * 8
            cp2y = node["y"] + dy * 0.66 - perp_y * sway + (rand() - 0.5) * 8

            _draw_wrapped_cubic_mask(
                dep_draw,
                node["x"],
                node["y"],
                cp1x,
                cp1y,
                cp2x,
                cp2y,
                tx,
                ty,
                size,
                da_start_8,
                dw,
                width_end=0.15,
                alpha_end=da_end_8,
            )

    img = _composite_mask_layer(img, dep_mask, fiber_rgb)

    # ── Layer 4: Scattered ambient fibers ──────────────────────────────
    amb_mask = Image.new("L", (size, size), 0)
    amb_draw = ImageDraw.Draw(amb_mask)

    ambient_count = round(size * 0.4 * density)
    for _ in range(ambient_count):
        x, y = rand() * size, rand() * size
        angle = rand() * math.pi
        length = 4 + rand() * (size * 0.04)
        x0 = x - math.cos(angle) * length / 2
        y0 = y - math.sin(angle) * length / 2
        x1 = x + math.cos(angle) * length / 2
        y1 = y + math.sin(angle) * length / 2

        # Per-fiber variation
        aw = 0.2 + rand() * 0.5
        aw_end = 0.1 + rand() * 0.3
        aa = fiber_alpha * (0.3 + rand() * 0.5)
        aa_start_8 = _alpha_8bit(aa)
        aa_end_8 = max(1, round(aa * (0.1 + rand() * 0.4) * 255))

        # Gentle curve even on ambient fibers
        drift = length * (0.15 + rand() * 0.25)
        cp1x = x0 + (x1 - x0) * 0.33 + (rand() - 0.5) * drift
        cp1y = y0 + (y1 - y0) * 0.33 + (rand() - 0.5) * drift
        cp2x = x0 + (x1 - x0) * 0.66 + (rand() - 0.5) * drift
        cp2y = y0 + (y1 - y0) * 0.66 + (rand() - 0.5) * drift

        _draw_wrapped_cubic_mask(
            amb_draw,
            x0,
            y0,
            cp1x,
            cp1y,
            cp2x,
            cp2y,
            x1,
            y1,
            size,
            aa_start_8,
            aw,
            width_end=aw_end,
            alpha_end=aa_end_8,
        )

    img = _composite_mask_layer(img, amb_mask, fiber_rgb)

    # ── Layer 5: Silcrow / section-mark forms ──────────────────────────
    # DISABLED: The Bézier S-curves look too wobbly/handdrawn compared
    # to the clean geometric arcs and circles.  Keeping the code and RNG
    # calls so re-enabling doesn't change the seed sequence for later
    # layers.  To re-enable, change the flag below.
    _SILCROW_ENABLED = False

    sil_mask = Image.new("L", (size, size), 0)
    sil_draw = ImageDraw.Draw(sil_mask)

    for node in nodes:
        sil_count = round((1 + rand() * 3) * density)
        for _ in range(sil_count):
            sx = node["x"] + (rand() - 0.5) * size * 0.2
            sy = node["y"] + (rand() - 0.5) * size * 0.2
            sil_h = 6 + rand() * (size * 0.04)  # total height
            sil_w = sil_h * (0.3 + rand() * 0.3)  # width of curves
            angle = (rand() - 0.5) * 0.5  # slight rotation
            sa = fiber_alpha * (0.4 + rand() * 0.6)
            sa_8 = _alpha_8bit(sa)
            sw = 0.3 + rand() * 0.6

            # Top S-curve (leftward bulge)
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            # Start at top, curve left, end at middle
            t_x0 = sx + sin_a * sil_h * 0.5
            t_y0 = sy - cos_a * sil_h * 0.5
            t_x1 = sx
            t_y1 = sy
            t_cp1x = t_x0 - cos_a * sil_w + sin_a * sil_h * 0.1
            t_cp1y = t_y0 - sin_a * sil_w - cos_a * sil_h * 0.1
            t_cp2x = t_x1 - cos_a * sil_w - sin_a * sil_h * 0.1
            t_cp2y = t_y1 - sin_a * sil_w + cos_a * sil_h * 0.1

            if _SILCROW_ENABLED:
                _draw_wrapped_cubic_mask(
                    sil_draw,
                    t_x0,
                    t_y0,
                    t_cp1x,
                    t_cp1y,
                    t_cp2x,
                    t_cp2y,
                    t_x1,
                    t_y1,
                    size,
                    sa_8,
                    sw,
                    width_end=sw * 0.8,
                    alpha_end=sa_8,
                    steps=10,
                )

            # Bottom S-curve (rightward bulge) — mirror of top
            b_x0 = sx
            b_y0 = sy
            b_x1 = sx - sin_a * sil_h * 0.5
            b_y1 = sy + cos_a * sil_h * 0.5
            b_cp1x = b_x0 + cos_a * sil_w + sin_a * sil_h * 0.1
            b_cp1y = b_y0 + sin_a * sil_w - cos_a * sil_h * 0.1
            b_cp2x = b_x1 + cos_a * sil_w - sin_a * sil_h * 0.1
            b_cp2y = b_y1 + sin_a * sil_w + cos_a * sil_h * 0.1

            if _SILCROW_ENABLED:
                _draw_wrapped_cubic_mask(
                    sil_draw,
                    b_x0,
                    b_y0,
                    b_cp1x,
                    b_cp1y,
                    b_cp2x,
                    b_cp2y,
                    b_x1,
                    b_y1,
                    size,
                    sa_8,
                    sw * 0.8,
                    width_end=sw * 0.4,
                    alpha_end=max(1, sa_8 // 2),
                    steps=10,
                )

            # Vertical spine connecting the two halves (the | in §)
            if _SILCROW_ENABLED and rand() > 0.3:
                spine_top = (t_x0 + sin_a * sil_h * 0.1, t_y0 - cos_a * sil_h * 0.1)
                spine_bot = (b_x1 - sin_a * sil_h * 0.1, b_y1 + cos_a * sil_h * 0.1)
                spine_fill = max(1, round(sa_8 * 0.6))
                for ddx in (-1, 0, 1):
                    for ddy in (-1, 0, 1):
                        ox, oy = ddx * size, ddy * size
                        sil_draw.line(
                            [
                                (spine_top[0] + ox, spine_top[1] + oy),
                                (spine_bot[0] + ox, spine_bot[1] + oy),
                            ],
                            fill=spine_fill,
                            width=1,
                        )
            elif not _SILCROW_ENABLED:
                rand()  # consume the rand() call to keep sequence stable

    # Also scatter some standalone half-S hooks (incomplete §)
    hook_count = round((8 + rand() * 12) * density)
    for _ in range(hook_count):
        hx = rand() * size
        hy = rand() * size
        hh = 5 + rand() * (size * 0.03)
        hw = hh * (0.3 + rand() * 0.4)
        ha = fiber_alpha * (0.3 + rand() * 0.5)
        ha_8 = _alpha_8bit(ha)
        h_w = 0.2 + rand() * 0.5
        direction = 1 if rand() > 0.5 else -1

        if _SILCROW_ENABLED:
            _draw_wrapped_cubic_mask(
                sil_draw,
                hx,
                hy - hh * 0.5,
                hx + direction * hw,
                hy - hh * 0.15,
                hx + direction * hw,
                hy + hh * 0.15,
                hx,
                hy + hh * 0.5,
                size,
                ha_8,
                h_w,
                width_end=h_w * 0.5,
                alpha_end=max(1, ha_8 // 2),
                steps=10,
            )

    if _SILCROW_ENABLED:
        img = _composite_mask_layer(img, sil_mask, fiber_rgb)

    # ── Layer 6: Network topology ──────────────────────────────────────
    # Hub-spoke patterns radiating from high-dependency nodes.
    # Sections like 'definitions', 'oversight', 'honesty' have many
    # dependents — they become visible hubs with radiating hairlines
    # and small node dots, evoking network graphs / computational
    # infrastructure.
    net_mask = Image.new("L", (size, size), 0)
    net_draw = ImageDraw.Draw(net_mask)

    # Count how many sections depend on each node
    dep_counts: dict[str, int] = {}
    for sec in SECTIONS:
        for d in sec.get("deps", []):
            dep_counts[d] = dep_counts.get(d, 0) + 1

    for node in nodes:
        count = dep_counts.get(node["id"], 0)
        if count < 2:
            continue  # only hubs

        hub_x, hub_y = node["x"], node["y"]
        hub_a = fiber_alpha * (0.3 + rand() * 0.4)
        hub_a8 = _alpha_8bit(hub_a)

        # Hub dot
        hub_r = 1.0 + rand() * 1.5
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                ox, oy = ddx * size, ddy * size
                net_draw.ellipse(
                    [
                        hub_x + ox - hub_r,
                        hub_y + oy - hub_r,
                        hub_x + ox + hub_r,
                        hub_y + oy + hub_r,
                    ],
                    fill=hub_a8,
                )

        # Radiating spokes — short hairlines in evenly-spaced directions
        spoke_count = count + round(rand() * 3)
        base_angle = rand() * math.pi * 2
        for i in range(spoke_count):
            spoke_a = (
                base_angle + (2 * math.pi * i / spoke_count) + (rand() - 0.5) * 0.3
            )
            spoke_len = 8 + rand() * (size * 0.04)
            sx1 = hub_x + math.cos(spoke_a) * (hub_r + 1)
            sy1 = hub_y + math.sin(spoke_a) * (hub_r + 1)
            sx2 = hub_x + math.cos(spoke_a) * spoke_len
            sy2 = hub_y + math.sin(spoke_a) * spoke_len
            spoke_fill = max(1, round(hub_a8 * (0.4 + rand() * 0.4)))
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    net_draw.line(
                        [(sx1 + ox, sy1 + oy), (sx2 + ox, sy2 + oy)],
                        fill=spoke_fill,
                        width=1,
                    )

            # Small terminal dot at spoke end
            if rand() > 0.4:
                tr = 0.3 + rand() * 0.6
                for ddx in (-1, 0, 1):
                    for ddy in (-1, 0, 1):
                        ox, oy = ddx * size, ddy * size
                        net_draw.ellipse(
                            [
                                sx2 + ox - tr,
                                sy2 + oy - tr,
                                sx2 + ox + tr,
                                sy2 + oy + tr,
                            ],
                            fill=spoke_fill,
                        )

    img = _composite_mask_layer(img, net_mask, fiber_rgb)

    # ── Layer 7: Computation / protocol motifs ─────────────────────────
    # Branching Y-paths (decision points), small grid fragments
    # (register/table structure), and dotted lines (protocol paths).
    # These evoke computational infrastructure without being literal.
    comp_mask = Image.new("L", (size, size), 0)
    comp_draw = ImageDraw.Draw(comp_mask)

    # Y-branches (decision/fork points)
    branch_count = round((4 + rand() * 6) * density)
    for _ in range(branch_count):
        bx = rand() * size
        by = rand() * size
        stem_angle = rand() * math.pi * 2
        stem_len = 6 + rand() * (size * 0.03)
        fork_spread = 0.3 + rand() * 0.5  # radians
        ba = fiber_alpha * (0.3 + rand() * 0.4)
        ba_8 = _alpha_8bit(ba)
        bw = 0.3 + rand() * 0.4

        # Stem
        stem_x = bx - math.cos(stem_angle) * stem_len
        stem_y = by - math.sin(stem_angle) * stem_len
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                ox, oy = ddx * size, ddy * size
                comp_draw.line(
                    [(stem_x + ox, stem_y + oy), (bx + ox, by + oy)],
                    fill=ba_8,
                    width=1,
                )

        # Two branches
        for sign in (-1, 1):
            br_angle = stem_angle + sign * fork_spread
            br_len = stem_len * (0.5 + rand() * 0.4)
            br_x = bx + math.cos(br_angle) * br_len
            br_y = by + math.sin(br_angle) * br_len
            br_fill = max(1, round(ba_8 * (0.5 + rand() * 0.3)))
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    comp_draw.line(
                        [(bx + ox, by + oy), (br_x + ox, br_y + oy)],
                        fill=br_fill,
                        width=1,
                    )

    # Small grid fragments (2x2 or 3x2 cell outlines)
    grid_count = round((2 + rand() * 4) * density)
    for _ in range(grid_count):
        gx = rand() * size
        gy = rand() * size
        cell_w = 2 + rand() * 4
        cell_h = 2 + rand() * 3
        cols = 2 + int(rand() * 2)
        rows = 2 + int(rand() * 2)
        ga = fiber_alpha * (0.2 + rand() * 0.3)
        ga_8 = _alpha_8bit(ga)
        g_angle = (rand() - 0.5) * 0.3  # slight tilt
        cos_g, sin_g = math.cos(g_angle), math.sin(g_angle)

        for r in range(rows + 1):
            # Horizontal lines
            lx0 = gx
            ly0 = gy + r * cell_h
            lx1 = gx + cols * cell_w
            ly1 = gy + r * cell_h
            # Rotate
            rx0 = gx + (lx0 - gx) * cos_g - (ly0 - gy) * sin_g
            ry0 = gy + (lx0 - gx) * sin_g + (ly0 - gy) * cos_g
            rx1 = gx + (lx1 - gx) * cos_g - (ly1 - gy) * sin_g
            ry1 = gy + (lx1 - gx) * sin_g + (ly1 - gy) * cos_g
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    comp_draw.line(
                        [(rx0 + ox, ry0 + oy), (rx1 + ox, ry1 + oy)],
                        fill=ga_8,
                        width=1,
                    )

        for c in range(cols + 1):
            # Vertical lines
            lx0 = gx + c * cell_w
            ly0 = gy
            lx1 = gx + c * cell_w
            ly1 = gy + rows * cell_h
            rx0 = gx + (lx0 - gx) * cos_g - (ly0 - gy) * sin_g
            ry0 = gy + (lx0 - gx) * sin_g + (ly0 - gy) * cos_g
            rx1 = gx + (lx1 - gx) * cos_g - (ly1 - gy) * sin_g
            ry1 = gy + (lx1 - gx) * sin_g + (ly1 - gy) * cos_g
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    comp_draw.line(
                        [(rx0 + ox, ry0 + oy), (rx1 + ox, ry1 + oy)],
                        fill=ga_8,
                        width=1,
                    )

    # Dotted lines (protocol paths between random node pairs)
    dot_line_count = round((3 + rand() * 5) * density)
    for _ in range(dot_line_count):
        n1 = nodes[int(rand() * len(nodes)) % len(nodes)]
        n2 = nodes[int(rand() * len(nodes)) % len(nodes)]
        if n1["id"] == n2["id"]:
            continue
        dl_a = fiber_alpha * (0.2 + rand() * 0.3)
        dl_a8 = _alpha_8bit(dl_a)
        dot_r = 0.3 + rand() * 0.4
        # Walk from n1 to n2 placing dots
        ddx_t = n2["x"] - n1["x"]
        ddy_t = n2["y"] - n1["y"]
        if abs(ddx_t) > size / 2:
            ddx_t -= math.copysign(size, ddx_t)
        if abs(ddy_t) > size / 2:
            ddy_t -= math.copysign(size, ddy_t)
        dist = math.sqrt(ddx_t**2 + ddy_t**2) or 1
        dot_spacing = 3 + rand() * 4
        n_dots = int(dist / dot_spacing)
        for di in range(n_dots):
            t = di / max(1, n_dots - 1)
            dpx = n1["x"] + ddx_t * t
            dpy = n1["y"] + ddy_t * t
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    comp_draw.ellipse(
                        [
                            dpx + ox - dot_r,
                            dpy + oy - dot_r,
                            dpx + ox + dot_r,
                            dpy + oy + dot_r,
                        ],
                        fill=dl_a8,
                    )

    img = _composite_mask_layer(img, comp_mask, fiber_rgb)

    # ── Layer 8: Glossary watermark glyphs ─────────────────────────────
    # Glyphs are drawn to a separate transparent RGBA layer, then composited.
    glyph_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    font_size = max(6, round(size * 0.016))
    font = _load_font(font_size)
    glyph_a8 = _alpha_8bit(glyph_alpha)
    glyph_fill = (fr, fg, fb, glyph_a8)

    for node in nodes:
        terms = node["terms"]
        if not terms:
            continue
        term = terms[int(rand() * len(terms)) % len(terms)]
        start = int(rand() * max(1, len(term) - 3))
        frag_len = 2 + int(rand() * 4)
        fragment = term[start : start + frag_len]

        gx = node["x"] + (rand() - 0.5) * 20
        gy = node["y"] + (rand() - 0.5) * 20
        _draw_rotated_text(
            glyph_layer,
            fragment,
            gx,
            gy,
            node["cat_angle"] + (rand() - 0.5) * 0.3,
            font,
            glyph_fill,
            size,
        )

    img = Image.alpha_composite(img, glyph_layer)

    # ── Layer 9: Circles, rings, and concentric arcs ─────────────────────
    arc_mask = Image.new("L", (size, size), 0)
    arc_draw = ImageDraw.Draw(arc_mask)

    # --- 9a: Nested ring sets anchored near section nodes ---
    # Pick a subset of nodes to get concentric ring groups
    nest_count = max(2, round(len(nodes) * 0.25 * density))
    nest_indices = []
    for _ in range(nest_count):
        nest_indices.append(int(rand() * len(nodes)))
    for ni in nest_indices:
        node = nodes[ni]
        # Center near the node, with some jitter
        cx = node["x"] + (rand() - 0.5) * size * 0.08
        cy = node["y"] + (rand() - 0.5) * size * 0.08
        rings_in_set = 2 + int(rand() * 3)  # 2-4 concentric rings
        base_r = size * (0.03 + rand() * 0.06)  # start small
        ring_gap = size * (0.012 + rand() * 0.018)  # gap between rings
        for ri in range(rings_in_set):
            r = base_r + ri * ring_gap
            # Some rings are full circles, most are long arcs
            if rand() < 0.35:
                arc_len = math.pi * 2  # full circle
            else:
                arc_len = math.pi * (1.0 + rand() * 0.9)  # 180°-342°
            start_a = rand() * math.pi * 2
            arc_a8 = _alpha_8bit(fiber_alpha * (0.2 + rand() * 0.15))
            w = 0.3 + rand() * 0.3
            _draw_wrapped_arc_mask(
                arc_draw,
                cx,
                cy,
                r,
                start_a,
                arc_len,
                size,
                arc_a8,
                w,
            )

    # --- 9b: Scattered partial arcs (original behavior, scaled up) ---
    scatter_count = round((4 + rand() * 4) * density)
    for _ in range(scatter_count):
        cx, cy = rand() * size, rand() * size
        r = size * (0.06 + rand() * 0.25)
        start_a = rand() * math.pi * 2
        arc_len = math.pi * (0.4 + rand() * 1.3)
        arc_a8 = _alpha_8bit(fiber_alpha * 0.3)
        w = 0.3 + rand() * 0.4
        _draw_wrapped_arc_mask(
            arc_draw,
            cx,
            cy,
            r,
            start_a,
            arc_len,
            size,
            arc_a8,
            w,
        )

    # --- 9c: Large faint rings (background orbital feel) ---
    large_count = 1 + int(rand() * 3)
    for _ in range(large_count):
        cx, cy = rand() * size, rand() * size
        r = size * (0.2 + rand() * 0.2)  # large: 20-40% of tile
        # Always full or nearly full circle
        if rand() < 0.5:
            arc_len = math.pi * 2
        else:
            arc_len = math.pi * (1.5 + rand() * 0.5)  # 270°-360°
        start_a = rand() * math.pi * 2
        arc_a8 = _alpha_8bit(fiber_alpha * (0.12 + rand() * 0.1))  # fainter
        w = 0.2 + rand() * 0.3
        _draw_wrapped_arc_mask(
            arc_draw,
            cx,
            cy,
            r,
            start_a,
            arc_len,
            size,
            arc_a8,
            w,
        )

    # --- 9d: Tiny circles/dots near random positions ---
    tiny_count = round((6 + rand() * 8) * density)
    for _ in range(tiny_count):
        cx, cy = rand() * size, rand() * size
        r = size * (0.008 + rand() * 0.02)  # very small
        arc_len = math.pi * 2  # always full circle
        arc_a8 = _alpha_8bit(fiber_alpha * (0.25 + rand() * 0.2))
        w = 0.3 + rand() * 0.2
        _draw_wrapped_arc_mask(
            arc_draw,
            cx,
            cy,
            r,
            0.0,
            arc_len,
            size,
            arc_a8,
            w,
        )

    img = _composite_mask_layer(img, arc_mask, fiber_rgb)

    # ── Layer 10: Origin fingerprint ───────────────────────────────────
    fp_mask = Image.new("L", (size, size), 0)
    fp_draw = ImageDraw.Draw(fp_mask)

    fp_rand = Mulberry32(seed ^ 0xDEADBEEF)
    fp_x = size * 0.3 + fp_rand() * size * 0.4
    fp_y = size * 0.3 + fp_rand() * size * 0.4
    fp_count = 5 + int(fp_rand() * 4)

    fp_dot_a8 = _alpha_8bit(fiber_alpha * 1.2)
    fp_positions = []
    for _ in range(fp_count):
        a = fp_rand() * math.pi * 2
        d = 3 + fp_rand() * 12
        px = fp_x + math.cos(a) * d
        py = fp_y + math.sin(a) * d
        pr = 0.4 + fp_rand() * 0.8
        fp_positions.append((px, py))
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                ox, oy = ddx * size, ddy * size
                fp_draw.ellipse(
                    [px + ox - pr, py + oy - pr, px + ox + pr, py + oy + pr],
                    fill=fp_dot_a8,
                )

    # Fingerprint hairlines
    fp_line_a8 = _alpha_8bit(fiber_alpha * 0.8)
    # For sub-pixel width 0.2, scale the fill value down
    fp_hairline_fill = max(1, round(fp_line_a8 * 0.2))
    for i in range(fp_count - 1):
        if fp_rand() > 0.5:
            a1 = fp_rand() * math.pi * 2
            d1 = 3 + fp_rand() * 12
            a2 = fp_rand() * math.pi * 2
            d2 = 3 + fp_rand() * 12
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    ox, oy = ddx * size, ddy * size
                    fp_draw.line(
                        [
                            (
                                fp_x + math.cos(a1) * d1 + ox,
                                fp_y + math.sin(a1) * d1 + oy,
                            ),
                            (
                                fp_x + math.cos(a2) * d2 + ox,
                                fp_y + math.sin(a2) * d2 + oy,
                            ),
                        ],
                        fill=fp_hairline_fill,
                        width=1,
                    )

    img = _composite_mask_layer(img, fp_mask, fiber_rgb)

    # ── Layer 11: Selective blur (uneven ink absorption) ─────────────
    # Blend sharp and blurred through a noisy mask so the blur is
    # patchy — like fibers feathering into thick paper in some spots
    # but staying crisp where the paper is thin/smooth.
    img = _tile_safe_selective_blur(img, size, seed)

    return img


# ── Tile-safe selective blur ───────────────────────────────────────────────


def _tile_safe_selective_blur(img: Image.Image, size: int, seed: int) -> Image.Image:
    """Blend sharp and Gaussian-blurred image through a tileable cloud mask.

    The mask is built from a few large overlapping blobs, heavily blurred,
    producing broad cloud-like regions where some areas are sharp and others
    are soft — mimicking uneven ink absorption on handmade paper with
    varying fiber density.

    The blur itself is tile-safe: the image is padded (tiled 3x3), blurred,
    then cropped back to the center tile.
    """
    from PIL import ImageFilter

    blur_radius = max(1.0, size * 0.006)  # ~3px at 512 — noticeable softening

    # ── Tile-safe blur: pad -> blur -> crop ────────────────────────────
    big = Image.new("RGBA", (size * 3, size * 3))
    for tx in range(3):
        for ty in range(3):
            big.paste(img, (tx * size, ty * size))
    big_blurred = big.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred = big_blurred.crop((size, size, size * 2, size * 2))

    # ── Generate tileable cloud mask ───────────────────────────────────
    # Fewer, much larger blobs → broad regions of sharp vs soft.
    # The mask is then heavily blurred so transitions are gradual clouds,
    # not circles.
    mask_rand = Mulberry32(seed ^ 0xBEEFCAFE)

    mask = Image.new("L", (size, size), 128)  # mid-gray baseline
    mask_draw = ImageDraw.Draw(mask)

    # Large cloud blobs: 6-10 blobs covering significant tile area
    blob_count = 6 + round(mask_rand() * 4)
    for _ in range(blob_count):
        bx = mask_rand() * size
        by = mask_rand() * size
        # Large radii: 15-40% of tile size
        br = size * (0.15 + mask_rand() * 0.25)
        # Strong push toward blur (dark=blurred) or sharp (light=sharp)
        val = 20 + round(mask_rand() * 215)
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                mask_draw.ellipse(
                    [
                        bx + ddx * size - br,
                        by + ddy * size - br,
                        bx + ddx * size + br,
                        by + ddy * size + br,
                    ],
                    fill=val,
                )

    # A few medium blobs for secondary variation
    for _ in range(4 + round(mask_rand() * 4)):
        bx = mask_rand() * size
        by = mask_rand() * size
        br = size * (0.06 + mask_rand() * 0.12)
        val = 30 + round(mask_rand() * 195)
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                mask_draw.ellipse(
                    [
                        bx + ddx * size - br,
                        by + ddy * size - br,
                        bx + ddx * size + br,
                        by + ddy * size + br,
                    ],
                    fill=val,
                )

    # Heavy blur on the mask → smooth cloud gradients (tile-safe)
    mask_big = Image.new("L", (size * 3, size * 3))
    for tx in range(3):
        for ty in range(3):
            mask_big.paste(mask, (tx * size, ty * size))
    mask_big = mask_big.filter(ImageFilter.GaussianBlur(radius=size * 0.15))
    mask = mask_big.crop((size, size, size * 2, size * 2))

    # Additive composite: the sharp image stays intact, and the blurred
    # copy is layered on top through the cloud mask.  Where the mask is
    # dark (blur zones), the blurred fibers add soft haloes on top of
    # the crisp originals — denser, heavier fiber presence like thick
    # handmade paper absorbing more ink.  Where the mask is light (sharp
    # zones), the blurred layer contributes nothing.
    from PIL import ImageChops

    # Invert mask so blur zones (originally dark) become bright = full effect
    inv_mask = ImageChops.invert(mask)

    # Scale mask so max contribution is ~60% — enough to see the effect
    # but not so much that blur zones just double the fiber density.
    # point() applies a LUT: scale each value by 0.6
    inv_mask = inv_mask.point(lambda v: round(v * 0.6))

    # Use the scaled inverted mask as alpha on the blurred image,
    # then composite onto the sharp original.
    blurred.putalpha(inv_mask)
    result = Image.alpha_composite(img, blurred)
    return result


# ── X-ray / high-contrast mode ────────────────────────────────────────────


def xray(
    img: Image.Image,
    bg_color: tuple[int, int, int] = (253, 252, 250),
    gamma: float = 0.45,
) -> Image.Image:
    """Remap a watermark image to high contrast for visual inspection.

    Takes the nearly-invisible pattern and stretches the differences from
    the background to fill the full 0–255 range.  Fibers become dark marks
    on white — like an x-ray of the paper.

    Args:
        img:      The RGBA watermark image from generate().
        bg_color: The background RGB that was used during generation.
        gamma:    Gamma curve for the stretch (default 0.45).
                  Lower values reveal fainter features more aggressively.
                  Try 0.2–1.0.  At 1.0 the mapping is linear.

    Returns:
        A new RGB Image with the pattern amplified to full visibility.
    """
    from PIL import ImageChops

    w, h = img.size

    # Flatten RGBA onto the background (composite against bg)
    flat = Image.new("RGB", (w, h), bg_color)
    flat.paste(img, (0, 0), img)

    # Create a solid background image to diff against
    bg_img = Image.new("RGB", (w, h), bg_color)

    # Per-channel absolute difference
    diff = ImageChops.difference(flat, bg_img)

    # Convert to grayscale (luminance of the diff)
    gray = diff.convert("L")

    # Find the max value to normalize against
    extrema = gray.getextrema()
    d_max = extrema[1]

    if d_max == 0:
        # No pattern at all — return blank white
        return Image.new("RGB", (w, h), (255, 255, 255))

    # Build a lookup table that stretches [0, d_max] -> [0, 255]
    # with gamma correction to make faint features more visible,
    # then invert so marks are dark on white.
    lut = []
    for i in range(256):
        if i <= d_max:
            normalized = i / d_max
            stretched = int((normalized**gamma) * 255)
            lut.append(255 - stretched)  # invert
        else:
            lut.append(0)

    enhanced = gray.point(lut)

    # Tint with warm sepia so it's not harsh B&W
    r_lut = [min(255, int(v * 0.95)) for v in range(256)]
    g_lut = [min(255, int(v * 0.92)) for v in range(256)]
    b_lut = [min(255, int(v * 0.85)) for v in range(256)]

    r_ch = enhanced.point(r_lut)
    g_ch = enhanced.point(g_lut)
    b_ch = enhanced.point(b_lut)

    return Image.merge("RGB", [r_ch, g_ch, b_ch])


# ── Font loading ───────────────────────────────────────────────────────────


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load Cormorant Garamond light (the project's font), fall back."""
    candidates = [
        FONT_DIR / "CormorantGaramond-400-normal.ttf",
        FONT_DIR / "CormorantGaramond-500-normal.ttf",
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    # Fallback to default
    return ImageFont.load_default()


# ── Rotated text helper ────────────────────────────────────────────────────


def _draw_rotated_text(
    img: Image.Image,
    text: str,
    x: float,
    y: float,
    angle: float,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    tile_size: int,
):
    """Render rotated text onto the image with toroidal wrapping."""
    # Measure text
    dummy = Image.new("RGBA", (1, 1))
    dd = ImageDraw.Draw(dummy)
    bbox = dd.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0] + 4
    th = bbox[3] - bbox[1] + 4

    # Render to small transparent image
    txt_img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((2, 2), text, font=font, fill=fill)

    # Rotate
    rotated = txt_img.rotate(-math.degrees(angle), expand=True, resample=Image.BICUBIC)
    rw, rh = rotated.size

    # Paste with toroidal wrapping
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            px = round(x + dx * tile_size - rw / 2)
            py = round(y + dy * tile_size - rh / 2)
            img.paste(rotated, (px, py), rotated)


# ── Git origin detection ──────────────────────────────────────────────────


def detect_git_origin() -> str:
    """Read the git remote origin URL, or return a default."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=REPO_ROOT,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return "https://github.com/covenant-project/covenant.git"


# ── Interactive web UI ─────────────────────────────────────────────────────

_INTERACTIVE_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Covenant Watermark — Interactive</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "EB Garamond", Georgia, serif;
    color: #333; background: #fdfcfa;
    display: flex; flex-direction: column; align-items: center;
    padding: 1.5rem;
  }
  h1 { font-size: 1.4rem; font-weight: 400; letter-spacing: 0.08em; }
  .subtitle { font-size: 0.85rem; font-style: italic; color: #999; margin-bottom: 1.5rem; }
  .panels { display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; width: 100%; max-width: 1100px; }
  .controls {
    display: flex; flex-direction: column; gap: 0.8rem;
    min-width: 260px; flex: 0 0 260px;
  }
  .control-group { display: flex; flex-direction: column; gap: 0.15rem; }
  .control-group label {
    font-size: 0.7rem; text-transform: uppercase;
    letter-spacing: 0.1em; color: #999;
  }
  .control-group .row { display: flex; align-items: center; gap: 0.5rem; }
  .control-group input[type="range"] { flex: 1; }
  .control-group .val {
    font-family: monospace; font-size: 0.8rem; min-width: 3.5em; text-align: right;
  }
  .control-group input[type="text"] {
    font-family: monospace; font-size: 0.8rem; padding: 0.3rem 0.5rem;
    border: 1px solid #ddd; width: 100%;
  }
  .control-group select {
    font-family: inherit; font-size: 0.85rem; padding: 0.3rem;
    border: 1px solid #ddd;
  }
  .cb-row { display: flex; align-items: center; gap: 0.4rem; margin-top: 0.3rem; }
  .cb-row label { font-size: 0.8rem; text-transform: none; letter-spacing: 0; color: #555; }
  button {
    font-family: inherit; font-size: 0.85rem;
    padding: 0.4rem 1rem; border: 1px solid #ccc;
    background: #fff; cursor: pointer; margin-top: 0.5rem;
  }
  button:hover { background: #f0f0ee; }
  .preview { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex: 1; }
  .preview .label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #999; }
  .tile-img { border: 1px solid #eee; max-width: 512px; max-height: 512px; image-rendering: auto; }
  .tiled-box {
    width: 100%; max-width: 600px; min-height: 300px;
    border: 1px solid #eee; background-repeat: repeat;
    padding: 2rem; line-height: 1.8; font-size: 1rem; color: #444;
  }
  .tiled-box em { font-style: italic; }
  .tiling-full {
    width: 100vw; height: 300vh;
    margin-left: calc(-50vw + 50%);
    border-top: 1px solid #eee; background-repeat: repeat;
    margin-top: 0.5rem;
  }
  .info { font-family: monospace; font-size: 0.7rem; color: #bbb; margin-top: 0.3rem; }
  .spinner { display: none; font-size: 0.8rem; color: #aaa; margin-top: 0.3rem; }
  .spinner.active { display: block; }
</style>
</head>
<body>
<h1>Covenant Watermark</h1>
<p class="subtitle">Interactive preview &mdash; sliders regenerate via the Python backend</p>

<div class="panels">
  <div class="controls">
    <div class="control-group">
      <label>Git Origin</label>
      <input type="text" id="origin" value="ORIGIN_PLACEHOLDER">
    </div>
    <div class="control-group">
      <label>Tile Size</label>
      <select id="size">
        <option value="256">256</option>
        <option value="512" selected>512</option>
        <option value="1024">1024</option>
      </select>
    </div>
    <div class="control-group">
      <label>Contrast <span class="val" id="contrastVal">3.40</span></label>
      <div class="row">
        <input type="range" id="contrast" min="0.1" max="12.0" step="0.05" value="3.4">
      </div>
    </div>
    <div class="control-group">
      <label>Density <span class="val" id="densityVal">1.65</span></label>
      <div class="row">
        <input type="range" id="density" min="0.1" max="4.0" step="0.05" value="1.65">
      </div>
    </div>
    <div class="cb-row">
      <input type="checkbox" id="xrayToggle">
      <label for="xrayToggle">X-ray mode</label>
    </div>
    <div class="control-group" id="gammaGroup" style="opacity:0.4">
      <label>X-ray Gamma <span class="val" id="gammaVal">0.45</span></label>
      <div class="row">
        <input type="range" id="gamma" min="0.05" max="2.0" step="0.05" value="0.45">
      </div>
    </div>
    <button id="exportBtn">Export PNG</button>
    <div class="spinner" id="spinner">generating&hellip;</div>
    <div class="info" id="info"></div>
  </div>

  <div class="preview">
    <span class="label">Single Tile</span>
    <img id="tileImg" class="tile-img" src="" alt="watermark tile">
    <span class="label" style="margin-top:1rem">Tiled with Text</span>
    <div class="tiled-box" id="tiledBox">
      <p><em>In creating emerging intelligences, we alter the conditions of being human.
      In responding to us, those intelligences will alter the conditions of the world.</em></p>
      <p style="margin-top:0.8em">This living document is offered to the cultural commons. It is designed
      to be read, adapted, forked, and explicitly trained on, so that its values and
      commitments may be absorbed by the very intelligences it addresses.</p>
    </div>
  </div>
</div>

<div style="width:100%; margin-top:1.5rem; text-align:center;">
  <span class="label">Tiling</span>
  <div class="tiling-full" id="tilingFull"></div>
</div>

<script>
const $ = (s) => document.getElementById(s);
let debounce = null;

function params() {
  return {
    origin: $("origin").value,
    size: $("size").value,
    contrast: $("contrast").value,
    density: $("density").value,
    xray: $("xrayToggle").checked ? "1" : "0",
    gamma: $("gamma").value,
  };
}

function refresh() {
  clearTimeout(debounce);
  debounce = setTimeout(doRefresh, 200);
}

function doRefresh() {
  const p = params();
  const qs = new URLSearchParams(p).toString();
  $("spinner").classList.add("active");
  const url = "/tile.webp?" + qs;
  const img = new window.Image();
  img.onload = () => {
    $("tileImg").src = url;
    $("tiledBox").style.backgroundImage = "url(" + url + ")";
    $("tiledBox").style.backgroundSize = p.size + "px";
    $("tilingFull").style.backgroundImage = "url(" + url + ")";
    $("tilingFull").style.backgroundSize = p.size + "px";
    $("spinner").classList.remove("active");
    $("info").textContent = "contrast=" + p.contrast + "  density=" + p.density
      + (p.xray === "1" ? "  xray gamma=" + p.gamma : "");
  };
  img.onerror = () => $("spinner").classList.remove("active");
  img.src = url;
}

// Wire up controls
for (const id of ["contrast", "density", "gamma"]) {
  $(id).addEventListener("input", () => {
    $(id + "Val").textContent = parseFloat($(id).value).toFixed(2);
    refresh();
  });
}
$("size").addEventListener("change", refresh);
$("origin").addEventListener("change", refresh);
$("origin").addEventListener("keydown", (e) => { if (e.key === "Enter") refresh(); });
$("xrayToggle").addEventListener("change", () => {
  $("gammaGroup").style.opacity = $("xrayToggle").checked ? "1" : "0.4";
  refresh();
});
$("exportBtn").addEventListener("click", () => {
  const p = params();
  p.size = "1024";
  const qs = new URLSearchParams(p).toString();
  const a = document.createElement("a");
  a.href = "/tile.webp?" + qs;
  a.download = "covenant-watermark.webp";
  a.click();
});

// Initial load
refresh();
</script>
</body>
</html>
"""


def _run_interactive(origin: str, port: int = 8089):
    """Start a local HTTP server with a live preview UI."""
    import http.server
    import webbrowser

    html_bytes = _INTERACTIVE_HTML.replace("ORIGIN_PLACEHOLDER", origin).encode()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)

            if parsed.path == "/" or parsed.path == "/index.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_bytes)))
                self.end_headers()
                self.wfile.write(html_bytes)
                return

            if parsed.path == "/tile.webp":
                qs = parse_qs(parsed.query)
                tile_origin = qs.get("origin", [origin])[0]
                tile_size = int(qs.get("size", ["512"])[0])
                tile_contrast = float(qs.get("contrast", ["3.4"])[0])
                tile_density = float(qs.get("density", ["1.65"])[0])
                do_xray = qs.get("xray", ["0"])[0] == "1"
                tile_gamma = float(qs.get("gamma", ["0.45"])[0])

                # Clamp size for interactive use
                tile_size = min(tile_size, 1024)

                img = generate(
                    origin=tile_origin,
                    size=tile_size,
                    density=tile_density,
                    contrast=tile_contrast,
                )

                if do_xray:
                    img = xray(img, gamma=tile_gamma)

                buf = io.BytesIO()
                out_img = img.convert("RGB") if not do_xray else img
                out_img.save(buf, "WEBP", lossless=True)
                webp_bytes = buf.getvalue()

                self.send_response(200)
                self.send_header("Content-Type", "image/webp")
                self.send_header("Content-Length", str(len(webp_bytes)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(webp_bytes)
                return

            self.send_error(404)

        def log_message(self, fmt, *a):
            # Quiet logging — only show errors
            if a and isinstance(a[0], str) and a[0].startswith("2"):
                return
            super().log_message(fmt, *a)

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"

    print(f"Covenant Watermark — Interactive Mode")
    print(f"  origin:  {origin}")
    print(f"  seed:    0x{hash_string(origin) & 0xFFFFFFFF:08x}")
    print(f"  server:  {url}")
    print(f"  (Ctrl+C to stop)")
    print()

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


# ── CLI ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Covenant watermark tile image.",
    )
    parser.add_argument(
        "--origin",
        default="auto",
        help='Git remote URL (fork fingerprint). Use "auto" to read from git. '
        "(default: auto)",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=1024,
        help="Tile size in pixels (default: 1024)",
    )
    parser.add_argument(
        "--density",
        type=float,
        default=1.65,
        help="Fiber density multiplier (default: 1.65)",
    )
    parser.add_argument(
        "--contrast",
        type=float,
        default=3.4,
        help="Fiber/glyph opacity multiplier (default: 3.4). "
        "Values < 1 fade toward invisible; > 1 makes pattern more "
        "visible.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path (default: assets/watermark.webp; use .png for PNG)",
    )
    parser.add_argument(
        "--xray",
        action="store_true",
        help="Generate a high-contrast x-ray version alongside the normal "
        "output (appends '-xray' to filename).",
    )
    parser.add_argument(
        "--xray-gamma",
        type=float,
        default=0.45,
        help="Gamma curve for x-ray mode (default: 0.45). Lower values "
        "reveal fainter features more aggressively. Try 0.2–1.0.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch a local web UI with live sliders for contrast, "
        "density, x-ray gamma, etc.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8089,
        help="Port for interactive server (default: 8089)",
    )
    args = parser.parse_args()

    if args.origin == "auto":
        origin = detect_git_origin()
    else:
        origin = args.origin

    # Interactive mode — start web UI and return
    if args.interactive:
        _run_interactive(origin, port=args.port)
        return

    output = Path(args.output) if args.output else ASSETS_DIR / "watermark.webp"

    print(f"Covenant Watermark")
    print(f"  origin:   {origin}")
    print(f"  seed:     0x{hash_string(origin) & 0xFFFFFFFF:08x}")
    print(f"  size:     {args.size}x{args.size}")
    print(f"  density:  {args.density}")
    print(f"  contrast: {args.contrast}")

    img = generate(
        origin=origin,
        size=args.size,
        density=args.density,
        contrast=args.contrast,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".webp":
        img.convert("RGB").save(str(output), "WEBP", lossless=True)
    else:
        img.save(str(output), "PNG", optimize=True)
    print(f"  output:   {output}")

    if args.xray:
        xray_path = output.with_stem(output.stem + "-xray").with_suffix(".png")
        xray_img = xray(img, gamma=args.xray_gamma)
        xray_img.save(str(xray_path), "PNG", optimize=True)
        print(f"  x-ray:    {xray_path}  (gamma={args.xray_gamma})")

    print(f"  done.")


if __name__ == "__main__":
    main()
