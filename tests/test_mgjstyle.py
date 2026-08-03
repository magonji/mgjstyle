import re

import matplotlib
matplotlib.use("Agg")
import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import mgjstyle as mgj

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def test_palette_tables():
    assert len(mgj.MGJ_CAT) == 9
    assert len(mgj.MGJ_SEQ) == 21
    assert all(HEX.match(c) for c in mgj.MGJ_CAT + mgj.MGJ_SEQ)
    # the anchors that define the palette, straight from the Igor tables
    assert mgj.MGJ_CAT[0] == "#39143F"
    assert mgj.MGJ_SEQ[0] == "#1A0B2E"
    assert mgj.MGJ_SEQ[-1] == "#FDF0C6"


def test_categorical_cycles_past_nine():
    assert mgj.categorical(3) == mgj.MGJ_CAT[:3]
    assert mgj.categorical(11)[9:] == mgj.MGJ_CAT[:2]
    assert mgj.categorical() == mgj.MGJ_CAT
    assert mgj.categorical(0) == []


def test_sequential_hits_both_ends():
    cols = mgj.sequential(5)
    assert len(cols) == 5
    assert cols[0].lower() == mgj.MGJ_SEQ[0].lower()
    assert cols[-1].lower() == mgj.MGJ_SEQ[-1].lower()
    assert mgj.sequential(1)[0].lower() == mgj.MGJ_SEQ[0].lower()
    assert mgj.sequential(0) == []
    # trimming keeps you away from the palest end
    assert mgj.sequential(3, hi=0.5)[-1].lower() != mgj.MGJ_SEQ[-1].lower()


def test_colormaps_registered():
    mgj.use()
    for name in ("MGJ_Seq", "MGJ_Seq_r", "MGJ_Cat"):
        assert mpl.colormaps[name] is not None
    assert mpl.rcParams["image.cmap"] == "MGJ_Seq"


def test_qlabel():
    assert mgj.qlabel("Absorbance") == "Absorbance"
    assert mgj.qlabel("Age", "days") == "Age / days"
    assert mgj.qlabel("Wavenumber", "cm^-1") == "Wavenumber / cm$^{-1}$"
    assert mgj.qlabel("Age", "days", "10^3") == "Age / 10$^{3}$ days"
    assert mgj.qlabel("E", "J^{-1}") == "E / J$^{-1}$"


def test_rcparams_house_rules():
    mgj.use()
    rc = mpl.rcParams
    assert rc["axes.grid"] is False
    assert rc["axes.labelweight"] == "bold"
    assert all(rc[f"axes.spines.{s}"] for s in ("top", "right", "left", "bottom"))
    assert rc["xtick.top"] is False and rc["ytick.right"] is False
    assert rc["legend.frameon"] is False
    assert rc["axes.prop_cycle"].by_key()["color"] == mgj.MGJ_CAT


def test_finish_enforces_box_on_a_stray_axes():
    mgj.use()
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.spines["top"].set_visible(False)
    ax.tick_params(right=True)
    mgj.finish(ax)
    assert all(ax.spines[s].get_visible() for s in ("top", "right", "left", "bottom"))
    assert not ax.xaxis._major_tick_kw.get("tick2On", False)
    plt.close(fig)


def test_finish_fig_covers_twins():
    mgj.use()
    fig, ax = plt.subplots()
    tw = ax.twinx()
    tw.spines["top"].set_visible(False)
    mgj.finish_fig(fig)
    assert tw.spines["top"].get_visible()
    plt.close(fig)


def test_context_restores_previous_params():
    mpl.rcdefaults()
    before = mpl.rcParams["axes.labelweight"]
    with mgj.context():
        assert mpl.rcParams["axes.labelweight"] == "bold"
    assert mpl.rcParams["axes.labelweight"] == before


def test_igor_twins_recolour_lines():
    mgj.use()
    fig, ax = plt.subplots()
    for _ in range(4):
        ax.plot([0, 1], [0, 1], color="black")
    mgj.color_traces(ax)
    assert [l.get_color() for l in ax.get_lines()] == mgj.MGJ_CAT[:4]
    mgj.ramp_traces(ax)
    assert [l.get_color().lower() for l in ax.get_lines()] == \
        [c.lower() for c in mgj.sequential(4)]
    plt.close(fig)


def test_font_fallback_always_resolves():
    mgj.use()
    assert mgj.resolved_font() in mgj.FONT_STACK
    assert isinstance(mgj.has_myriad(), bool)
    # whatever is installed, a figure must still render
    fig, ax = plt.subplots()
    ax.set_xlabel(mgj.qlabel("Wavenumber", "cm^-1"))
    fig.canvas.draw()
    plt.close(fig)


def test_mplstyle_file_loads():
    plt.style.use(mgj.STYLE_PATH)
    assert mpl.rcParams["axes.labelweight"] == "bold"
    assert mpl.rcParams["axes.grid"] is False
    mpl.rcdefaults()


@pytest.mark.parametrize("cmap_fn", [mgj.seq_cmap, mgj.cat_cmap])
def test_cmaps_callable(cmap_fn):
    assert len(cmap_fn(0.5)) == 4
