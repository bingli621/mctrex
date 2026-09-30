"""
Plot the guide layout of a McStas instrument (side view, top view, element index),
colouring every guide wall by its m-value.

Reads the .instr file directly: resolves AT/ROTATED ... RELATIVE chains, applies WHEN
conditions for the given instrument parameters, and marks NXdisk_chopper positions.
Chopper labels give the flight path along the beam in m.

Usage:
    python plot_guide_gravity.py                             # default: jupyter/trex/mcstas/trex_primary.instr
    python plot_guides.py trex_primary.instr                 # bender = 0 (file default)
    python plot_guides.py trex_primary.instr --set bender=1  # bender in
    python plot_guides.py trex_primary.instr -o layout.png
"""

import argparse
import re
from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap

# jupyter/trex/mcstas/trex_primary.instr, resolved relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INSTR = SCRIPT_DIR.parent / "trex" / "mcstas" / "trex_primary.instr"
DEFAULT_OUT = SCRIPT_DIR / "guide_layout.png"
SAVE_DPI = 600

# ----------------------------------------------------------------------------- parsing


def strip_comments(txt):
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", txt)


def split_top(s, sep=","):
    """Split on sep, ignoring separators inside (), {} and quotes."""
    out, depth, buf, q = [], 0, "", False
    for ch in s:
        if ch == '"':
            q = not q
        elif not q and ch in "({":
            depth += 1
        elif not q and ch in ")}":
            depth -= 1
        if ch == sep and depth == 0 and not q:
            out.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


def evaluate(expr, env):
    try:
        return eval(
            expr.replace("==", " == ").replace("&&", " and ").replace("||", " or "),
            {"__builtins__": {}},
            env,
        )
    except Exception:
        return expr.strip()


def parse_instr(path, overrides):
    txt = strip_comments(open(path).read())

    # instrument parameters (defaults), then user overrides
    env = {"PI": np.pi}
    m = re.search(
        r"DEFINE\s+INSTRUMENT\s+\w+\s*\((.*?)\)\s*(DECLARE|INITIALIZE|TRACE)",
        txt,
        re.DOTALL,
    )
    if m:
        for p in split_top(m.group(1)):
            if "=" in p:
                lhs, rhs = p.split("=", 1)
                env[lhs.split()[-1]] = evaluate(rhs.strip(), env)
    env.update(overrides)

    # simple scalar assignments in DECLARE (for L_* phasing distances)
    declare = {}
    m = re.search(r"DECLARE\s*%\{(.*?)%\}", txt, re.DOTALL)
    if m:
        for name, val in re.findall(
            r"double\s+(\w+)\s*=\s*([-+0-9.eE]+)\s*;", m.group(1)
        ):
            declare[name] = float(val)

    trace = txt[txt.index("TRACE") :]
    comp_re = re.compile(
        r"(?:SPLIT\s*\d*\s*)?COMPONENT\s+(\w+)\s*=\s*(\w+)\s*\((.*?)\)\s*"
        r"(?:WHEN\s*\((.*?)\)\s*)?"
        r"AT\s*\(([^)]*)\)\s*(ABSOLUTE|RELATIVE\s+\w+)\s*"
        r"(?:ROTATED\s*\(([^)]*)\)\s*(ABSOLUTE|RELATIVE\s+\w+))?",
        re.DOTALL,
    )
    comps = OrderedDict()
    for name, ctype, params, when, at, at_ref, rot, rot_ref in comp_re.findall(trace):
        pdict = {}
        for p in split_top(params):
            if "=" in p:
                k, v = p.split("=", 1)
                pdict[k.strip()] = evaluate(v.strip(), env)
        comps[name] = dict(
            type=ctype,
            params=pdict,
            active=bool(evaluate(when, env)) if when else True,
            at=[float(evaluate(x, env)) for x in split_top(at)],
            at_ref=at_ref.split()[-1],
            rot=[float(evaluate(x, env)) for x in split_top(rot)] if rot else [0, 0, 0],
            rot_ref=(rot_ref or at_ref).split()[-1],
        )
    return comps, declare, env


# ----------------------------------------------------------------------------- geometry


def rotmat(rx, ry, rz):
    """McStas ROTATED (rx, ry, rz) in degrees, as a local->reference matrix."""
    ax, ay, az = np.radians([rx, ry, rz])
    Rx = np.array(
        [[1, 0, 0], [0, np.cos(ax), -np.sin(ax)], [0, np.sin(ax), np.cos(ax)]]
    )
    Ry = np.array(
        [[np.cos(ay), 0, np.sin(ay)], [0, 1, 0], [-np.sin(ay), 0, np.cos(ay)]]
    )
    Rz = np.array(
        [[np.cos(az), -np.sin(az), 0], [np.sin(az), np.cos(az), 0], [0, 0, 1]]
    )
    return Rz @ Ry @ Rx


def resolve(comps):
    for name, c in comps.items():
        if c["at_ref"] == "ABSOLUTE":
            P0, R0 = np.zeros(3), np.eye(3)
        else:
            P0, R0 = comps[c["at_ref"]]["pos"], comps[c["at_ref"]]["R"]
        RR = np.eye(3) if c["rot_ref"] == "ABSOLUTE" else comps[c["rot_ref"]]["R"]
        c["pos"] = P0 + R0 @ np.array(c["at"])
        c["R"] = RR @ rotmat(*c["rot"])


def guide_geometry(c):
    p = c["params"]
    if c["type"] == "Pol_bender":
        w1 = w2 = p["xwidth"]
        h1 = h2 = p["yheight"]
        L = p["length"]
        m = dict(mleft=np.nan, mright=np.nan, mtop=np.nan, mbottom=np.nan)
    else:
        w1, h1, w2, h2, L = (p[k] for k in ("w1", "h1", "w2", "h2", "l"))
        m = {k: p.get(k, p.get("m", 1)) for k in ("mleft", "mright", "mtop", "mbottom")}
    P, R = c["pos"], c["R"]
    g = lambda x, y, z: P + R @ np.array([x, y, z])
    return dict(
        L=L,
        m=m,
        left=(g(w1 / 2, 0, 0), g(w2 / 2, 0, L)),
        right=(g(-w1 / 2, 0, 0), g(-w2 / 2, 0, L)),
        top=(g(0, h1 / 2, 0), g(0, h2 / 2, L)),
        bottom=(g(0, -h1 / 2, 0), g(0, -h2 / 2, L)),
        z0=g(0, 0, 0)[2],
        z1=g(0, 0, L)[2],
    )


def path_lengths(comps):
    """Flight distance along the beam to each active component (through guide exits)."""
    skip = {"Monitor_nD", "Progress_bar", "Diag"}
    pts, prev, s, out = [], np.zeros(3), 0.0, {}
    for name, c in comps.items():
        if not c["active"] or c["type"] in skip:
            continue
        s += np.linalg.norm(c["pos"] - prev)
        prev = c["pos"]
        out[name] = s
        if "geom" in c:
            exitp = c["pos"] + c["R"] @ np.array([0, 0, c["geom"]["L"]])
            s += np.linalg.norm(exitp - prev)
            prev = exitp
    return out


# ----------------------------------------------------------------------------- plotting

M_VALUES = np.arange(1.0, 5.01, 0.5)
# tab10 without red, matching the reference figure (1 blue, 1.5 orange, 2 green, 2.5 purple ...)
M_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
CMAP = ListedColormap(M_COLORS)
NORM = BoundaryNorm(np.append(M_VALUES - 0.25, M_VALUES[-1] + 0.25), CMAP.N)
BENDER_COLOR = "black"
WALL = 0.35  # drawn wall thickness in cm


def wall(ax, a, b, idx, mval, lw=3.2):
    """Draw one wall from a to b as a thick segment (z in m, transverse in cm)."""
    col = BENDER_COLOR if np.isnan(mval) else CMAP(NORM(mval))
    ax.plot(
        [a[2], b[2]],
        [a[idx] * 100, b[idx] * 100],
        color=col,
        lw=lw,
        solid_capstyle="butt",
    )


def short_label(name):
    m = re.match(r"(?i)guide_(.+)", name)
    return m.group(1) if m else name


def chopper_groups(comps, dist, declare):
    ch = [
        (n, c)
        for n, c in comps.items()
        if c["type"] == "NXdisk_chopper" and c["active"]
    ]
    groups = []
    for n, c in ch:
        if groups and abs(c["pos"][2] - groups[-1][-1][1]["pos"][2]) < 0.5:
            groups[-1].append((n, c))
        else:
            groups.append([(n, c)])
    out = []
    for g in groups:
        pref = re.match(r"([A-Za-z]+)", g[0][0]).group(1)
        pref = {"BW": "BW", "PS": "PSC", "MC": "MC"}.get(pref, pref)
        nums = [
            re.findall(r"(\d+)$", n)[0] if re.findall(r"(\d+)$", n) else ""
            for n, _ in g
        ]
        phased = []
        for n, c in g:
            d = c["params"].get("delay")
            key = (
                "L_" + d.split("delay_")[-1]
                if isinstance(d, str) and "delay_" in d
                else None
            )
            phased.append(declare.get(key))
        if len(g) == 1:
            lab = pref + nums[0]
        else:
            lab = pref + ",".join(nums)
            lab = pref + nums[0] + "," + ",".join(nums[1:])
        out.append(
            dict(
                label=lab,
                z=[c["pos"][2] for _, c in g],
                s=[dist[n] for n, _ in g],
                phased=phased,
            )
        )
    return out


def plot(comps, declare, env, outfile, title=None):
    guides = [
        (n, c)
        for n, c in comps.items()
        if c["active"] and c["type"] in ("Guide_gravity", "Guide", "Pol_bender")
    ]
    for n, c in guides:
        c["geom"] = guide_geometry(c)
    dist = path_lengths(comps)

    fig = plt.figure(figsize=(10, 6), dpi=200)
    gs = fig.add_gridspec(
        3,
        2,
        height_ratios=[1, 1.2, 0.95],
        width_ratios=[1, 0.018],
        hspace=0.12,
        wspace=0.03,
        left=0.075,
        right=0.915,
        top=0.86,
        bottom=0.115,
    )
    ax_s = fig.add_subplot(gs[0, 0])
    ax_t = fig.add_subplot(gs[1, 0], sharex=ax_s)
    ax_i = fig.add_subplot(gs[2, 0], sharex=ax_s)
    cax = fig.add_subplot(gs[0:2, 1])

    for n, c in guides:
        g = c["geom"]
        wall(ax_s, *g["top"], 1, g["m"]["mtop"])
        wall(ax_s, *g["bottom"], 1, g["m"]["mbottom"])
        # side view: all rotations are about y, so the entrance/exit faces are vertical here
        for i in (0, 1):
            a, b = g["top"][i], g["bottom"][i]
            ax_s.plot(
                [a[2], b[2]],
                [a[1] * 100, b[1] * 100],
                color="black",
                lw=0.6,
                alpha=0.4,
                zorder=1,
            )

    zmax = max(c["geom"]["z1"] for _, c in guides)
    ax_s.set_xlim(-3, zmax + 5)
    ax_s.set_ylim(-5.9, 5.9)
    xs = (
        np.concatenate(
            [
                [c["geom"]["left"][i][0], c["geom"]["right"][i][0]]
                for _, c in guides
                for i in (0, 1)
            ]
        )
        * 100
    )
    pad = 0.12 * (xs.max() - xs.min())
    ax_t.set_ylim(xs.min() - pad, xs.max() + pad)

    # top view: entrance/exit faces are perpendicular to each guide's own axis.
    # The true tilt (< 0.5 mm in z) is invisible at this aspect ratio, so each face is
    # drawn perpendicular to the guide axis *as displayed* (exact x, exaggerated z), and the
    # left/right walls are drawn between the ends of those faces so everything joins up.
    fig.canvas.draw()
    T = ax_t.transData

    def face(c, i):
        g = c["geom"]
        ax_dir = c["R"] @ np.array([0, 0, 1.0])  # guide axis, global
        L, R = g["left"][i], g["right"][i]
        ctr = (L + R) / 2
        p0 = T.transform([ctr[2], ctr[0] * 100])
        p1 = T.transform([ctr[2] + ax_dir[2], (ctr[0] + ax_dir[0]) * 100])
        d = (p1 - p0) / np.linalg.norm(p1 - p0)  # axis direction on screen
        perp = np.array([-d[1], d[0]])
        k = (T.transform([ctr[2], L[0] * 100])[1] - p0[1]) / perp[1]
        return T.inverted().transform(
            [p0 + k * perp, p0 - k * perp]
        )  # [left end, right end]

    for n, c in guides:
        g = c["geom"]
        f_in, f_out = face(c, 0), face(c, 1)
        for j, side in ((0, "mleft"), (1, "mright")):
            m = g["m"][side]
            col = BENDER_COLOR if np.isnan(m) else CMAP(NORM(m))
            ax_t.plot(
                [f_in[j, 0], f_out[j, 0]],
                [f_in[j, 1], f_out[j, 1]],
                color=col,
                lw=1.6,
                solid_capstyle="butt",
            )
        for f in (f_in, f_out):
            ax_t.plot(f[:, 0], f[:, 1], color="black", lw=0.6, alpha=0.4, zorder=3)
    ax_s.set_ylabel("position  ( cm )")
    ax_t.set_ylabel("position  ( cm )")
    ax_s.text(
        0.015,
        0.94,
        "Side view",
        transform=ax_s.transAxes,
        ha="left",
        va="top",
        fontsize=12,
    )
    ax_t.text(
        0.015,
        0.94,
        "Top view",
        transform=ax_t.transAxes,
        ha="left",
        va="top",
        fontsize=12,
    )
    plt.setp(ax_s.get_xticklabels(), visible=False)
    plt.setp(ax_t.get_xticklabels(), visible=False)

    # choppers
    groups = chopper_groups(comps, dist, declare)
    for gi, grp in enumerate(groups):
        zc = np.mean(grp["z"])
        ha = "center"
        if gi + 1 < len(groups) and np.mean(groups[gi + 1]["z"]) - zc < 15:
            ha = "right"
        elif gi > 0 and zc - np.mean(groups[gi - 1]["z"]) < 15:
            ha = "left"
        for ax in (ax_s, ax_t):
            ax.axvline(zc, ls="--", color="0.3", lw=1)
        pos_txt = "/".join(
            f"{s:.3f}".rstrip("0").rstrip(".")
            if abs(s - round(s, 2)) < 5e-4
            else f"{s:.3f}"
            for s in grp["s"]
        )
        lab = f"{grp['label']}\n{pos_txt}"
        ax_s.text(
            zc,
            1.04,
            lab,
            transform=ax_s.get_xaxis_transform(),
            ha=ha,
            va="bottom",
            fontsize=9,
        )

    # colour bar
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=NORM)
    cb = fig.colorbar(sm, cax=cax, ticks=M_VALUES)
    cb.set_ticklabels([f"{v:g}" for v in M_VALUES])
    cb.set_label("coating value", rotation=270, labelpad=18, fontsize=13)

    # element index strip
    nrows = 6
    for k, (n, c) in enumerate(guides):
        g = c["geom"]
        row = k % nrows
        col = BENDER_COLOR if c["type"] == "Pol_bender" else "#5d6d7e"
        ax_i.plot(
            [g["z0"], g["z1"]], [row, row], lw=3, color=col, solid_capstyle="butt"
        )
        ax_i.text(
            (g["z0"] + g["z1"]) / 2,
            row + 0.3,
            short_label(n),
            ha="center",
            va="bottom",
            fontsize=4.5,
        )
    ax_i.set_ylim(-0.6, nrows + 0.2)
    ax_i.set_yticks([])
    for sp in ("left", "right", "top"):
        ax_i.spines[sp].set_visible(False)
    ax_i.set_ylabel("guide\nindex", rotation=0, ha="right", va="center", fontsize=11)
    ax_i.text(
        0,
        1.0,
        "element index — the component is  Guide_<index>",
        transform=ax_i.transAxes,
        fontsize=7,
        color="0.35",
        va="bottom",
    )
    ax_i.set_xlabel("position  ( m )", fontsize=12)

    note = [f"bender = {env.get('bender')}"] if "bender" in env else []
    if any(c["type"] == "Pol_bender" for _, c in guides):
        note.append("black = Pol_bender")
    if note:
        fig.text(0.075, 0.008, ",  ".join(note), fontsize=7, color="0.35")
    if title:
        fig.suptitle(title, y=0.995, fontsize=11)
    fig.savefig(outfile, dpi=SAVE_DPI)
    return guides, dist


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instr", nargs="?", default=str(DEFAULT_INSTR))
    ap.add_argument("-o", "--out", default=str(DEFAULT_OUT))
    ap.add_argument(
        "--set",
        action="append",
        default=[],
        help="override instrument parameter, e.g. --set bender=1",
    )
    ap.add_argument("--title", default=None)
    a = ap.parse_args()
    ov = {}
    for s in a.set:
        k, v = s.split("=", 1)
        ov[k] = evaluate(v, {})
    comps, declare, env = parse_instr(a.instr, ov)
    resolve(comps)
    guides, dist = plot(comps, declare, env, a.out, a.title)
    print(
        f"{len(guides)} guide elements, last exit at z = "
        f"{max(c['geom']['z1'] for _, c in guides):.3f} m"
    )
    for n, c in comps.items():
        if c["type"] == "NXdisk_chopper":
            print(
                f"  {n:14s} z = {c['pos'][2]:9.4f} m   flight path = {dist[n]:9.4f} m"
            )


if __name__ == "__main__":
    main()
