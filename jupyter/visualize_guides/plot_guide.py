"""T-REX guide profile: side view, top view, and element index.

Reads the CAD guide meshes (Guide_anyshape_r OFF files) and draws the beamline
coloured by supermirror coating value, with every chopper marked, the optical
assemblies named, and each guide element labelled by its instrument index.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm, ListedColormap

M_LEVELS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
M_COLOURS = ["C0", "C1", "C2", "C4", "C5", "C6", "C7", "C8", "C9"]


def m_colour(value):
    """Map a coating value in [1, 5] onto the default colour cycle."""
    return M_COLOURS[round((value - 1.0) * 2)]


# Every chopper in the instrument, as (z / m, label).  The P and M discs are
# 100 mm and 10 mm apart respectively, so each pair is treated as one and
# shares a single label at the pair's mid-point.
CHOPPER_LABELS = [
    (32.0, "BW1\n32.0"),
    (40.0, "BW2\n40.0"),
    (108.0, "PSC1,2\n107.95/108.05"),
    (162.0, "MC1,2\n161.995/162.005"),
]

# L_FO, from the instrument's DECLARE block.
FO_Z = 151.51801


def load(directory):
    segs = []
    for p in Path(directory).glob("try*.off"):
        # skip try4_.OFF
        if p.stem == "try4_":
            continue
        # read all lines
        lines = [
            l
            for l in p.read_text().splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
        v = np.array([[float(x) for x in lines[2 + i].split()[:3]] for i in range(8)])
        m = {}
        for i in range(4):
            raw = lines[10 + i]
            m[raw.split("#")[1].strip()] = float(raw.split("#")[0].split()[5])
        entry, exit_ = v[:4], v[4:]
        segs.append(
            dict(
                index=int(p.stem[3:]),
                z=(entry[:, 2].mean(), exit_[:, 2].mean()),
                xlo=(entry[:, 0].min(), exit_[:, 0].min()),
                xhi=(entry[:, 0].max(), exit_[:, 0].max()),
                ylo=(entry[:, 1].min(), exit_[:, 1].min()),
                yhi=(entry[:, 1].max(), exit_[:, 1].max()),
                m=m,
            )
        )
    segs.sort(key=lambda s: s["z"][0])
    return segs


def gap_around(segs, z):
    """Edges (z_before, z_after) of the guide gap that straddles ``z``."""
    ends_before = [s["z"][1] for s in segs if s["z"][1] <= z]
    starts_after = [s["z"][0] for s in segs if s["z"][0] >= z]
    z_before = max(ends_before) if ends_before else z
    z_after = min(starts_after) if starts_after else z
    return z_before, z_after


def add_walls(ax, segs, lo_key, hi_key, lo_face, hi_face, lw=3.2):
    for key, face in ((lo_key, lo_face), (hi_key, hi_face)):
        pts = [
            [[s["z"][0], s[key][0] * 100], [s["z"][1], s[key][1] * 100]] for s in segs
        ]
        cols = [m_colour(s["m"][face]) for s in segs]
        ax.add_collection(
            LineCollection(pts, colors=cols, linewidths=lw, capstyle="butt", zorder=4)
        )


def chopper_lines(ax, segs, y0, y1, colour="0.35"):
    # Two dashed lines per chopper location, at the edges of the guide gap the
    # chopper sits in, so the pair brackets the gap width.
    for z, _ in CHOPPER_LABELS:
        for zz in gap_around(segs, z):
            ax.plot([zz, zz], [y0, y1], ls=(0, (5, 4)), lw=0.9, color=colour, zorder=2)
    ax.plot([FO_Z, FO_Z], [y0, y1], ls=(0, (2, 3)), lw=1.1, color="#c26a00", zorder=2)


def main(off_directory):
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="trex_guide_profile.png")
    args = ap.parse_args()

    segs = load(off_directory)
    z1 = max(s["z"][1] for s in segs)

    fig = plt.figure(figsize=(10, 6), dpi=200)
    fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(
        3,
        2,
        width_ratios=[1, 0.01],
        height_ratios=[1.0, 1.22, 0.80],
        left=0.072,
        right=0.912,
        top=0.868,
        bottom=0.078,
        hspace=0.13,
        wspace=0.045,
    )
    ax_s = fig.add_subplot(gs[0, 0])
    ax_t = fig.add_subplot(gs[1, 0], sharex=ax_s)
    ax_i = fig.add_subplot(gs[2, 0], sharex=ax_s)
    ax_c = fig.add_subplot(gs[:2, 1])

    # ---------------- side view ----------------
    add_walls(ax_s, segs, "ylo", "yhi", "bottom", "top")
    ax_s.set_ylim(-5.9, 5.9)
    ax_s.set_yticks([-4, -2, 0, 2, 4])
    ax_s.set_ylabel("position  ( cm )", fontsize=10.5)
    ax_s.text(
        0.988,
        0.06,
        "Side view",
        transform=ax_s.transAxes,
        ha="right",
        va="bottom",
        fontsize=11.5,
    )
    chopper_lines(ax_s, segs, -5.9, 5.9)
    plt.setp(ax_s.get_xticklabels(), visible=False)

    # ---------------- top view ----------------
    add_walls(ax_t, segs, "xlo", "xhi", "right", "left")
    ax_t.set_ylim(-11, 91)
    ax_t.set_yticks([0, 20, 40, 60, 80])
    ax_t.set_ylabel("position  ( cm )", fontsize=10.5)
    ax_t.text(
        0.988,
        0.06,
        "Top view",
        transform=ax_t.transAxes,
        ha="right",
        va="bottom",
        fontsize=11.5,
    )
    chopper_lines(ax_t, segs, -11, 91)
    plt.setp(ax_t.get_xticklabels(), visible=False)

    # ---------------- chopper + gap labels ----------------
    for z, text in CHOPPER_LABELS:
        ax_s.annotate(
            text,
            xy=(z, 5.9),
            xytext=(z, 7.2),
            ha="center",
            va="bottom",
            fontsize=8.5,
            annotation_clip=False,
            linespacing=1.35,
        )

    # ---------------- element index strip ----------------
    for s in segs:
        lvl = s["index"] % 6
        ax_i.plot(
            s["z"], [lvl, lvl], lw=2.4, solid_capstyle="butt", color="#5a6672", zorder=3
        )
        ax_i.text(
            sum(s["z"]) / 2,
            lvl + 0.18,
            str(s["index"]),
            fontsize=3.5,
            ha="center",
            va="bottom",
            color="0.12",
        )
    ax_i.set_ylim(-0.6, 6.8)
    ax_i.set_yticks([])
    ax_i.set_xlabel("position  ( m )", fontsize=10.5)
    ax_i.set_ylabel(
        "guide\nindex", fontsize=9, labelpad=16, rotation=0, va="center", ha="center"
    )
    ax_i.text(
        0.002,
        1.005,
        "element index — the component is  guide_<index>",
        transform=ax_i.transAxes,
        ha="left",
        va="bottom",
        fontsize=7.6,
        color="0.35",
    )
    for sp in ("top", "right", "left"):
        ax_i.spines[sp].set_visible(False)

    for ax in (ax_s, ax_t, ax_i):
        ax.set_xlim(-2, z1 + 4)
        ax.tick_params(labelsize=9.5, direction="out", length=3)
        for sp in ax.spines.values():
            sp.set_linewidth(0.9)

    # ---------------- colour bar ----------------
    cmap = ListedColormap(M_COLOURS)
    bounds = [v - 0.25 for v in M_LEVELS] + [M_LEVELS[-1] + 0.25]
    cb = fig.colorbar(
        plt.cm.ScalarMappable(norm=BoundaryNorm(bounds, cmap.N), cmap=cmap),
        cax=ax_c,
        ticks=M_LEVELS,
        spacing="uniform",
    )
    cb.ax.set_yticklabels([f"{v:g}" for v in M_LEVELS], fontsize=10)
    cb.outline.set_linewidth(0.9)
    cb.set_label("coating value", fontsize=12.5, rotation=270, labelpad=22)

    output = Path(args.output)
    if not output.is_absolute():
        output = Path(__file__).resolve().parent / output
    fig.savefig(output, facecolor="white")
    print(f"wrote {output}  ({len(segs)} elements)")
    plt.show()


if __name__ == "__main__":
    off_directory = Path("./src/OFF_files_swap")
    main(off_directory)
