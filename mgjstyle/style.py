"""The MGJ figure style: rcParams, axis labels, and per-axes finishing.

House rules
-----------
* Axes are drawn as a full **box** — all four spines, with the top and right
  acting as mirror axes: no ticks, no labels there.
* **No grid.** Ever.
* Font **Myriad**, with a graceful fallback (see :mod:`mgjstyle.fonts`).
* Axis **labels bold**, tick numbers normal weight.
* Units go **after a slash**: ``Age / days`` — the plotted numbers are the
  quantity divided by its unit. A scale factor divides too, and comes first:
  ``qlabel("Age", "days", "10^3")`` -> ``Age / 10³ days``.
* Colours from the MGJ palette (:mod:`mgjstyle.colors`).
"""

from __future__ import annotations

import contextlib
import os
import shutil

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

from . import colors as _c
from . import fonts as _f

__all__ = ["rc_params", "use", "apply", "context", "finish", "finish_fig",
           "qlabel", "color_traces", "ramp_traces", "install_mplstyle",
           "STYLE_PATH"]

#: Path to the plain ``.mplstyle`` file (a subset — see :func:`use`).
STYLE_PATH = os.path.join(os.path.dirname(__file__), "mgj.mplstyle")


def rc_params(font_size: float = 11, linewidth: float = 1.0,
              dpi: int = 200) -> dict:
    """The MGJ rcParams as a plain dict, so you can inspect or tweak them."""
    return {
        "font.family": "sans-serif",
        "font.sans-serif": _f.FONT_STACK,
        "font.size": font_size,
        "axes.titlesize": font_size * 1.05,
        "axes.labelsize": font_size,
        "xtick.labelsize": font_size * 0.9,
        "ytick.labelsize": font_size * 0.9,
        "legend.fontsize": font_size * 0.9,

        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "figure.dpi": dpi,
        "savefig.dpi": dpi,
        "savefig.bbox": "tight",

        # the box: four spines; mirror axes carry no ticks and no labels
        "axes.spines.top": True, "axes.spines.right": True,
        "axes.spines.left": True, "axes.spines.bottom": True,
        "axes.edgecolor": _c.INK, "axes.linewidth": linewidth,
        "axes.grid": False,

        "axes.labelweight": "bold",     # labels bold, tick numbers not
        "axes.labelcolor": _c.INK,
        "axes.titleweight": "normal", "axes.titlecolor": _c.INK,
        "text.color": _c.INK,

        "xtick.color": _c.INK, "ytick.color": _c.INK,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.top": False, "ytick.right": False,
        "xtick.major.size": 4, "ytick.major.size": 4,
        "xtick.minor.size": 2, "ytick.minor.size": 2,
        "xtick.major.width": linewidth, "ytick.major.width": linewidth,

        "lines.linewidth": 1.6,
        "lines.markersize": 5,
        "legend.frameon": False,

        "axes.prop_cycle": cycler(color=_c.MGJ_CAT),
        "image.cmap": "MGJ_Seq",
    }


def use(font_size: float = 11, linewidth: float = 1.0, dpi: int = 200,
        warn_font: bool = False) -> None:
    """Apply the MGJ style globally: fonts, colormaps and rcParams.

    Prefer this over ``plt.style.use`` — only this path can register the
    colormaps and find Myriad. Set ``warn_font=True`` to be told when Myriad
    is missing and which face is standing in for it.
    """
    _c.register_colormaps()
    _f.register_local_fonts()
    if warn_font:
        _f.warn_if_no_myriad()
    mpl.rcParams.update(rc_params(font_size, linewidth, dpi))


#: Alias kept for scripts written against the original ``mgj_style.apply()``.
apply = use


@contextlib.contextmanager
def context(**kwargs):
    """Use the style for one block only::

        with mgj.context():
            fig, ax = plt.subplots()
    """
    _c.register_colormaps()
    _f.register_local_fonts()
    with mpl.rc_context(rc_params(**kwargs)):
        yield


def install_mplstyle() -> str:
    """Copy ``mgj.mplstyle`` into matplotlib's config dir.

    Afterwards ``plt.style.use("mgj")`` works anywhere — handy in notebooks,
    though it cannot register the colormaps, so :func:`use` remains the
    complete option. Returns the destination path.
    """
    dest_dir = os.path.join(mpl.get_configdir(), "stylelib")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "mgj.mplstyle")
    shutil.copyfile(STYLE_PATH, dest)
    plt.style.reload_library()
    return dest


# --- axis labels ------------------------------------------------------------

import re as _re


def _superscript(s):
    """Caret exponents -> mathtext superscripts, which render in any font
    (Myriad has no unicode superscript-minus): ``cm^-1`` -> ``cm$^{-1}$``.
    Handles both ``^{...}`` and bare ``^-12``."""
    if s is None:
        return None
    s = _re.sub(r"\^\{([^}]*)\}", r"$^{\1}$", str(s))
    s = _re.sub(r"\^(-?\d+)", r"$^{\1}$", s)
    return s


def qlabel(name: str, unit: str | None = None, scale: str | None = None) -> str:
    """``'name / [scale] unit'`` — the MGJ divided-unit axis label.

    ``qlabel("Wavenumber", "cm^-1")`` -> ``Wavenumber / cm⁻¹``
    ``qlabel("Age", "days", "10^3")`` -> ``Age / 10³ days``
    ``qlabel("Absorbance")``          -> ``Absorbance`` (dimensionless)
    """
    if unit is None and scale is None:
        return name
    parts = [p for p in (_superscript(scale), _superscript(unit)) if p]
    return f"{name} / {' '.join(parts)}"


# --- per-axes finishing -----------------------------------------------------

def finish(*axes, linewidth: float = 1.0) -> None:
    """Enforce the box, kill the grid, keep ticks on bottom/left only.

    Call it after plotting. rcParams cover axes you create yourself, but not
    twin axes, insets, seaborn output, or pandas' ``df.plot()`` — this does.
    With no arguments it finishes the current axes.
    """
    axes = axes or (plt.gca(),)
    for ax in axes:
        ax.grid(False)
        for side in ("top", "right", "left", "bottom"):
            ax.spines[side].set_visible(True)
            ax.spines[side].set_edgecolor(_c.INK)
            ax.spines[side].set_linewidth(linewidth)
        ax.tick_params(top=False, right=False, which="both")
        ax.tick_params(labeltop=False, labelright=False)


def finish_fig(fig=None, linewidth: float = 1.0) -> None:
    """:func:`finish` every axes in a figure (current figure by default)."""
    fig = fig or plt.gcf()
    finish(*fig.get_axes(), linewidth=linewidth)


# --- Igor twins -------------------------------------------------------------

def color_traces(ax=None) -> None:
    """Recolour the lines of *ax* with the categorical palette, in order.

    The twin of Igor's ``MGJ_ColorTraces``: useful when the lines were drawn
    by code you do not control (seaborn, pandas) and so missed the cycler.
    """
    ax = ax or plt.gca()
    lines = ax.get_lines()
    for i, line in enumerate(lines):
        line.set_color(_c.MGJ_CAT[i % len(_c.MGJ_CAT)])


def ramp_traces(ax=None, lo: float = 0.0, hi: float = 1.0) -> None:
    """Recolour the lines of *ax* along the sequential ramp, in order.

    The twin of Igor's ``MGJ_RampTraces``, for ordered series.
    """
    ax = ax or plt.gca()
    lines = ax.get_lines()
    for line, col in zip(lines, _c.sequential(len(lines), lo, hi)):
        line.set_color(col)
