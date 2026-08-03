#!/usr/bin/env python3
"""Render examples/gallery.png — every part of the style in one figure.

    python examples/gallery.py
"""
import os

import matplotlib.pyplot as plt
import numpy as np

import mgjstyle as mgj

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    mgj.use()
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))

    # 1 — categorical series: different kinds of thing
    ax = axes[0, 0]
    x = np.linspace(0, 2 * np.pi, 200)
    for i in range(5):
        ax.plot(x, np.sin(x + i * 0.5), label=f"series {i + 1}")
    ax.set_xlabel(mgj.qlabel("Time", "s"))
    ax.set_ylabel(mgj.qlabel("Signal", "V", "10^-3"))
    ax.set_title("Categorical palette")
    ax.set_ylim(-1.7, 1.15)
    ax.legend(ncol=3, loc="lower center", fontsize=8)

    # 2 — sequential ramp: ordered series (here, ageing spectra)
    ax = axes[0, 1]
    wn = np.linspace(1800, 900, 400)
    n = 9
    for i, col in enumerate(mgj.sequential(n, hi=0.85)):
        y = (np.exp(-((wn - 1650) / 40) ** 2) * (1 - 0.06 * i)
             + np.exp(-((wn - 1080) / 30) ** 2) * (0.4 + 0.07 * i))
        ax.plot(wn, y, color=col, label=f"{i * 3} d" if i in (0, n - 1) else None)
    ax.invert_xaxis()
    ax.set_xlabel(mgj.qlabel("Wavenumber", "cm^-1"))
    ax.set_ylabel(mgj.qlabel("Absorbance"))
    ax.set_title("Sequential ramp")
    ax.legend(loc="upper right")

    # 3 — scatter coloured by a quantity
    ax = axes[0, 2]
    x = rng.normal(size=250)
    y = x * 0.8 + rng.normal(scale=0.6, size=250)
    sc = ax.scatter(x, y, c=x + y, cmap="MGJ_Seq", s=22, edgecolor="none")
    fig.colorbar(sc, ax=ax, label=mgj.qlabel("Score"))
    ax.set_xlabel(mgj.qlabel("Measured age", "days"))
    ax.set_ylabel(mgj.qlabel("Predicted age", "days"))
    ax.set_title("Scatter + colormap")

    # 4 — bars with the semantic roles
    ax = axes[1, 0]
    names = ["baseline", "tuned", "transfer", "wild"]
    vals = [0.62, 0.78, 0.55, 0.31]
    cols = [mgj.MUTED, mgj.DEEP, mgj.POS, mgj.NEG]
    ax.bar(names, vals, color=cols, edgecolor=mgj.INK, linewidth=0.6)
    ax.axhline(0.5, color=mgj.MUTED, ls="--", lw=1)
    ax.set_ylabel(mgj.qlabel("R²"))
    ax.set_title("Semantic roles")

    # 5 — heatmap in a single hue
    ax = axes[1, 1]
    z = np.outer(np.hanning(20), np.hanning(20)) + rng.normal(scale=0.05, size=(20, 20))
    im = ax.imshow(z, cmap=mgj.mono_cmap(mgj.PRIMARY), aspect="auto")
    fig.colorbar(im, ax=ax, label=mgj.qlabel("Intensity", "a.u."))
    ax.set_xlabel(mgj.qlabel("Column"))
    ax.set_ylabel(mgj.qlabel("Row"))
    ax.set_title("mono_cmap")

    # 6 — the palette itself
    ax = axes[1, 2]
    for i, c in enumerate(mgj.MGJ_CAT):
        ax.add_patch(plt.Rectangle((i, 1.15), 0.92, 0.75, color=c))
    for i, c in enumerate(mgj.MGJ_SEQ):
        ax.add_patch(plt.Rectangle((i * 9 / 21, 0.1), 9 / 21, 0.75, color=c))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.1)
    ax.set_xticks([])
    ax.set_yticks([1.5, 0.5])
    ax.set_yticklabels(["MGJ_CAT", "MGJ_SEQ"])
    ax.set_title("The palette")

    mgj.finish_fig(fig)
    fig.tight_layout()
    out = os.path.join(HERE, "gallery.png")
    fig.savefig(out, dpi=150)
    print(f"font in use: {mgj.resolved_font()}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
