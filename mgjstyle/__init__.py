"""mgjstyle — Mario González-Jiménez's matplotlib palette and figure style.

    import matplotlib.pyplot as plt
    import mgjstyle as mgj

    mgj.use()

    fig, ax = plt.subplots()
    ax.plot(x, y, color=mgj.PRIMARY)
    ax.set_xlabel(mgj.qlabel("Wavenumber", "cm^-1"))
    ax.set_ylabel(mgj.qlabel("Absorbance"))
    mgj.finish(ax)
"""

from .colors import (MGJ_CAT, MGJ_SEQ, PRIMARY, DEEP, POS, NEG, GOLD, MUTED,
                     INK, cat_cmap, seq_cmap, seq_cmap_r, categorical,
                     sequential, mono_cmap, register_colormaps)
from .fonts import (FONT_STACK, add_font_dir, available_fonts, has_myriad,
                    register_local_fonts, resolved_font)
from .style import (STYLE_PATH, apply, color_traces, context, finish,
                    finish_fig, install_mplstyle, qlabel, ramp_traces,
                    rc_params, use)

__version__ = "0.1.0"

__all__ = [
    # palette
    "MGJ_CAT", "MGJ_SEQ", "PRIMARY", "DEEP", "POS", "NEG", "GOLD", "MUTED",
    "INK", "cat_cmap", "seq_cmap", "seq_cmap_r", "categorical", "sequential",
    "mono_cmap", "register_colormaps",
    # fonts
    "FONT_STACK", "add_font_dir", "available_fonts", "has_myriad",
    "register_local_fonts", "resolved_font",
    # style
    "use", "apply", "context", "rc_params", "finish", "finish_fig", "qlabel",
    "color_traces", "ramp_traces", "install_mplstyle", "STYLE_PATH",
    "__version__",
]
