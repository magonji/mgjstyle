"""Font resolution for the MGJ style.

The house font is **Myriad Pro**. It ships with Adobe products, so most people
will not have it — and matplotlib does not index Adobe's OTFs automatically
even on machines that do. This module therefore:

1. registers any Myriad OTF/TTF found in the usual font directories, and
2. exposes a fallback stack of humanist sans faces, ending at DejaVu Sans,
   which ships with matplotlib and is always present.

So the style always renders; it just looks its best where Myriad exists.
:func:`resolved_font` tells you which face you actually got.
"""

from __future__ import annotations

import glob
import os
import warnings

import matplotlib.font_manager as fm

__all__ = ["FONT_STACK", "register_local_fonts", "add_font_dir",
           "available_fonts", "resolved_font", "has_myriad", "warn_if_no_myriad"]

#: Preferred families, best first. Source Sans 3 is the free face closest to
#: Myriad (same designer lineage); the rest are common humanist sans fallbacks.
FONT_STACK = [
    "Myriad Pro", "Myriad",
    "Source Sans 3", "Source Sans Pro",
    "Avenir Next", "Avenir",
    "Open Sans", "Lato", "PT Sans",
    "Helvetica Neue", "Arial",
    "DejaVu Sans",          # always available (bundled with matplotlib)
]

_FONT_DIRS = [
    os.path.expanduser("~/Library/Fonts"),      # macOS, user
    "/Library/Fonts", "/System/Library/Fonts",  # macOS, system
    os.path.expanduser("~/.fonts"),             # Linux, user
    os.path.expanduser("~/.local/share/fonts"),
    "/usr/share/fonts", "/usr/local/share/fonts",
    os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"),  # Windows
    r"C:\Windows\Fonts",
]

_PATTERNS = ("Myriad*.otf", "Myriad*.ttf", "MyriadPro-*.otf", "SourceSans3-*.otf",
             "SourceSans3-*.ttf", "SourceSansPro-*.otf", "SourceSansPro-*.ttf")


def add_font_dir(path: str) -> int:
    """Register every font file in *path* (recursively) with matplotlib.

    Returns how many files were added. Use this if your fonts live somewhere
    unusual, e.g. ``add_font_dir("~/fonts/myriad")``.
    """
    added = 0
    root = os.path.expanduser(path)
    for pattern in ("*.otf", "*.ttf", "*.ttc"):
        for f in glob.glob(os.path.join(root, "**", pattern), recursive=True):
            try:
                fm.fontManager.addfont(f)
                added += 1
            except Exception:  # unreadable / unsupported file — skip quietly
                pass
    return added


def register_local_fonts() -> None:
    """Look for Myriad (and Source Sans) in the standard font directories."""
    have = available_fonts()
    if "Myriad Pro" in have and "Source Sans 3" in have:
        return
    for d in _FONT_DIRS:
        if not d or not os.path.isdir(d):
            continue
        for pattern in _PATTERNS:
            for f in glob.glob(os.path.join(d, pattern)):
                try:
                    fm.fontManager.addfont(f)
                except Exception:
                    pass


def available_fonts() -> set[str]:
    """Family names matplotlib currently knows about."""
    return {f.name for f in fm.fontManager.ttflist}


def resolved_font() -> str:
    """The first family in :data:`FONT_STACK` that is actually installed."""
    have = available_fonts()
    for name in FONT_STACK:
        if name in have:
            return name
    return "DejaVu Sans"


def has_myriad() -> bool:
    """True if Myriad is installed and visible to matplotlib."""
    have = available_fonts()
    return "Myriad Pro" in have or "Myriad" in have


def warn_if_no_myriad() -> None:
    """Emit a one-line warning naming the substitute font in use."""
    if not has_myriad():
        warnings.warn(
            f"mgjstyle: Myriad not found, using {resolved_font()!r} instead. "
            "Install Myriad Pro or Source Sans 3 for the intended look.",
            stacklevel=2,
        )
