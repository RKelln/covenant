#!/usr/bin/env python3
"""
install_fonts.py — Install Cormorant Garamond fonts for use with WeasyPrint.

WeasyPrint uses the system font stack (Pango/fontconfig on Linux, CoreText on
macOS, GDI+ on Windows). CSS @font-face declarations are silently ignored in
PDF output. Fonts must be installed to the OS font directory.

Usage:
    uv run python build/install_fonts.py
    python build/install_fonts.py   (if venv is active)

Supports: Linux, macOS, Windows (per-user install, no admin required).
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_SRC = REPO_ROOT / "assets" / "fonts"

FONT_FILES = [
    "CormorantGaramond-400-normal.ttf",
    "CormorantGaramond-400-italic.ttf",
    "CormorantGaramond-500-normal.ttf",
    "CormorantGaramond-500-italic.ttf",
    "CormorantGaramond-600-normal.ttf",
    "CormorantGaramond-600-italic.ttf",
]


def get_font_dir() -> Path:
    system = platform.system()
    if system == "Linux":
        return Path.home() / ".local" / "share" / "fonts" / "CormorantGaramond"
    elif system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    elif system == "Windows":
        # Per-user install — no admin required (Windows 10+)
        local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return local / "Microsoft" / "Windows" / "Fonts"
    else:
        print(f"Unknown platform: {system}")
        sys.exit(1)


def refresh_font_cache(system: str, font_dir: Path) -> None:
    if system == "Linux":
        print("Refreshing fontconfig cache...")
        result = subprocess.run(["fc-cache", "-fv"], capture_output=True, text=True)
        if result.returncode == 0:
            print("  fc-cache: OK")
        else:
            print(f"  fc-cache warning: {result.stderr.strip()}")
    elif system == "Darwin":
        # macOS picks up fonts in ~/Library/Fonts automatically; no cache step needed.
        # Optionally activate via atsutil but that's unnecessary for most cases.
        print("  macOS: fonts will be available after next app launch (no cache step needed).")
    elif system == "Windows":
        # Register fonts in the per-user registry so apps can find them.
        try:
            import winreg
            reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                for f in FONT_FILES:
                    font_path = font_dir / f
                    # Registry value name — strip extension, human-readable
                    name = f.replace("CormorantGaramond-", "Cormorant Garamond ").replace(".ttf", "")
                    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, str(font_path))
            print("  Windows registry: font entries written.")
        except Exception as e:
            print(f"  Windows registry warning: {e}")
            print("  You may need to double-click each font file to install manually.")


def verify_installation(system: str) -> None:
    """Quick sanity check that fonts are findable."""
    if system == "Linux":
        result = subprocess.run(
            ["fc-list", ":family=Cormorant Garamond"],
            capture_output=True, text=True
        )
        found = [l for l in result.stdout.strip().splitlines() if l]
        if found:
            print(f"\nVerification: {len(found)} Cormorant Garamond faces found by fontconfig.")
            for line in found:
                print(f"  {line}")
        else:
            print("\nVerification: fontconfig cannot find Cormorant Garamond yet.")
            print("  Try running 'fc-cache -fv' manually, then check with 'fc-list | grep Cormorant'.")
    elif system == "Darwin":
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType"],
            capture_output=True, text=True
        )
        if "Cormorant" in result.stdout:
            print("\nVerification: Cormorant Garamond found by macOS font system.")
        else:
            print("\nVerification: cannot confirm via system_profiler — fonts may need an app restart.")
    elif system == "Windows":
        print("\nVerification: check Start → Settings → Fonts and search 'Cormorant'.")


def main() -> None:
    system = platform.system()
    font_dir = get_font_dir()

    print(f"Platform : {system}")
    print(f"Font src : {FONTS_SRC}")
    print(f"Font dst : {font_dir}")
    print()

    # Check source files exist
    missing = [f for f in FONT_FILES if not (FONTS_SRC / f).exists()]
    if missing:
        print("ERROR: Missing font files in assets/fonts/:")
        for f in missing:
            print(f"  {f}")
        print("\nRe-clone the repository or download Cormorant Garamond from:")
        print("  https://github.com/CatharsisFonts/Cormorant/releases")
        sys.exit(1)

    # Create destination directory
    font_dir.mkdir(parents=True, exist_ok=True)

    # Copy fonts
    installed = 0
    skipped = 0
    for fname in FONT_FILES:
        src = FONTS_SRC / fname
        dst = font_dir / fname
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"  skip  {fname}  (up to date)")
            skipped += 1
        else:
            shutil.copy2(src, dst)
            print(f"  copy  {fname}")
            installed += 1

    print(f"\n{installed} installed, {skipped} already up to date.")

    if installed > 0:
        refresh_font_cache(system, font_dir)
    else:
        print("Nothing to do.")

    verify_installation(system)

    print("\nDone. Run 'make pdf' to verify the fonts appear in the output:")
    print("  pdffonts dist/covenant.ritual.pdf | grep -i cormorant")


if __name__ == "__main__":
    main()
