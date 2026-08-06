"""MGJ colour palette.

Two tables, ported one-to-one from the Igor Pro procedure
``MGJ_MakeColorTables``:

* ``MGJ_CAT`` — 9 categorical colours, for series that are *different kinds*
  of thing (species, treatments, models).
* ``MGJ_SEQ`` — a 21-step sequential ramp (dark plum -> orange -> cream), for
  quantities that are *ordered* (age, dose, time, intensity).

Everything else here is convenience: named roles, colormaps, and helpers that
sample either table for an arbitrary number of series.
"""

from __future__ import annotations

import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

__all__ = [
    "MGJ_CAT", "MGJ_SEQ", "PRIMARY", "DEEP", "POS", "NEG", "GOLD", "MUTED",
    "INK", "cat_cmap", "seq_cmap", "seq_cmap_r", "categorical", "sequential",
    "mono_cmap", "register_colormaps",
]

# --- the tables -------------------------------------------------------------

#: Categorical palette (9 colours), in order.
MGJ_CAT = [
    "#960B00",  # 0 dark red
    "#FEC830",  # 1 gold
    "#818D29",  # 2 olive
    "#0F69B5",  # 3 blue
    "#39143F",  # 4 dark plum
    "#8B9083",  # 5 grey-green
    "#3A6260",  # 6 teal-green
    "#66A7C9",  # 7 light blue
    "#52051A",  # 8 wine
    
]

#: Sequential ramp (21 steps), dark -> light.
MGJ_SEQ = [
    "#1A0B2E", "#28103F", "#381451", "#4B185D", "#601C64", "#75216B",
    "#8A286A", "#9E2F69", "#B03B65", "#C04B5D", "#D05A55", "#DA6E50",
    "#E38149", "#EB9348", "#EFA34F", "#F4B455", "#F7C36A", "#F8D27F",
    "#FADE95", "#FCE7AE", "#FDF0C6",
]

# --- semantic roles ---------------------------------------------------------

PRIMARY = MGJ_CAT[3]   #: default accent — one series, one colour
DEEP = MGJ_CAT[4]      #: emphasis — the highlighted / winning case
POS = MGJ_CAT[6]       #: "good", improvement
NEG = MGJ_CAT[0]       #: "bad", loss
GOLD = MGJ_CAT[1]      #: attention, annotation
MUTED = MGJ_CAT[5]     #: context, reference lines, ignored series
INK = "#201018"      #: text, axes and ticks (a near-black with a plum cast)

# --- colormaps --------------------------------------------------------------

seq_cmap = LinearSegmentedColormap.from_list("MGJ_Seq", MGJ_SEQ)
seq_cmap_r = seq_cmap.reversed()  # name: MGJ_Seq_r
cat_cmap = ListedColormap(MGJ_CAT, name="MGJ_Cat")


def register_colormaps() -> None:
    """Make ``'MGJ_Seq'``, ``'MGJ_Seq_r'`` and ``'MGJ_Cat'`` usable by name.

    Called for you by :func:`mgjstyle.use`; safe to call repeatedly.
    """
    for cm in (seq_cmap, seq_cmap_r, cat_cmap):
        try:
            if cm.name in mpl.colormaps:
                continue          # already there; re-registering only warns
            mpl.colormaps.register(cm)
        except (ValueError, AttributeError):  # older matplotlib
            pass


def mono_cmap(color: str | None = None, name: str = "MGJ_mono",
              light: str = "white") -> LinearSegmentedColormap:
    """Single-hue ramp ``light`` -> ``color``.

    For a magnitude that should stay in one colour (e.g. a heatmap that must
    match the series it belongs to). Defaults to the primary blue.
    """
    return LinearSegmentedColormap.from_list(name, [light, color or PRIMARY])


# --- sampling helpers -------------------------------------------------------

def categorical(n: int | None = None) -> list[str]:
    """First *n* categorical colours (cycling past 9, as Igor's ``mod`` does)."""
    if n is None:
        return list(MGJ_CAT)
    if n < 0:
        raise ValueError("n must be >= 0")
    return [MGJ_CAT[i % len(MGJ_CAT)] for i in range(n)]


def sequential(n: int, lo: float = 0.0, hi: float = 1.0) -> list[str]:
    """*n* colours evenly spaced along the sequential ramp.

    The Python twin of Igor's ``MGJ_RampTraces``: use it when the series are
    ordered (ages, concentrations, days). ``lo``/``hi`` trim the ends of the
    ramp — ``sequential(n, hi=0.85)`` drops the palest colours, which is worth
    doing for thin lines on white.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return []
    if n == 1:
        return [mpl.colors.to_hex(seq_cmap(lo))]
    step = (hi - lo) / (n - 1)
    return [mpl.colors.to_hex(seq_cmap(lo + i * step)) for i in range(n)]
