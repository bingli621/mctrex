from mctrex.mcstas_components import Arm, Guide_gravity, gap
from mctrex.params.guides_curve import guide_29


def chain_guide_straight(current, previous):
    """Place `current` right after `previous`; the axis is straight here, so no tilt."""
    current.AT = [0, 0, previous.l + gap(previous, current)]
    current.RELATIVE = previous.name
    return current


# =============================================================================
# End of the 12 km curve at Guide_29 (T1 @ 96 m) - straight from here on, so
# every joint below is a plain z-translation with no ROTATED component.
# =============================================================================

guide_30 = Guide_gravity(
    name="Guide_30",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.997000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=96.002550,
    z2=99.999550,
)
chain_guide_straight(guide_30, guide_29)

guide_31 = Guide_gravity(
    name="Guide_31",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.997000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=100.002550,
    z2=103.999550,
)
chain_guide_straight(guide_31, guide_30)

guide_32 = Guide_gravity(
    name="Guide_32",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.893750,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=104.002550,
    z2=107.896300,
)
chain_guide_straight(guide_32, guide_31)

# PSC Gap: 200 mm slot for the P-Chopper pair (ToO: "P-Chopper (Pos.: 108m)").
# A branch off Guide_32, same pattern as arm_bm1 in guides_curve.py - it
# doesn't sit inline in the main chain, so Guide_33 below still chains
# directly off Guide_32.
arm_psc = Arm(
    name="Arm_PSC",
    l=0.200000,
    z1=107.900000,
    z2=108.100000,
)
chain_guide_straight(arm_psc, guide_32)

guide_33 = Guide_gravity(
    name="Guide_33",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=2.994300,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=108.103700,
    z2=111.098000,
)
chain_guide_straight(guide_33, arm_psc)

# Gap 33->34 holds Beam Monitor 2 ("Gap BM2"); see monitors.py for BM1's
# equivalent pattern if BM2 gets added the same way.
# Guides 34-44 approximate two elliptic sections as short straight (chord)
# segments, same technique used for the 12 km curve.
guide_34 = Guide_gravity(
    name="Guide_34",
    w1=0.060129,
    h1=0.085000,
    w2=0.064343,
    h2=0.085000,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=111.098000,
    z2=115.098000,
)
chain_guide_straight(guide_34, guide_33)

guide_35 = Guide_gravity(
    name="Guide_35",
    w1=0.064343,
    h1=0.085000,
    w2=0.067329,
    h2=0.085000,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=115.098000,
    z2=119.098000,
)
chain_guide_straight(guide_35, guide_34)

guide_36 = Guide_gravity(
    name="Guide_36",
    w1=0.067329,
    h1=0.085000,
    w2=0.069247,
    h2=0.085000,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=119.098000,
    z2=123.098000,
)
chain_guide_straight(guide_36, guide_35)

guide_37 = Guide_gravity(
    name="Guide_37",
    w1=0.069247,
    h1=0.085000,
    w2=0.069542,
    h2=0.085000,
    l=0.902000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=123.098000,
    z2=124.000000,
)
chain_guide_straight(guide_37, guide_36)

guide_38 = Guide_gravity(
    name="Guide_38",
    w1=0.069542,
    h1=0.084998,
    w2=0.070266,
    h2=0.084562,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=124.000000,
    z2=128.000000,
)
chain_guide_straight(guide_38, guide_37)

guide_39 = Guide_gravity(
    name="Guide_39",
    w1=0.070266,
    h1=0.084562,
    w2=0.070052,
    h2=0.083340,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=128.000000,
    z2=132.000000,
)
chain_guide_straight(guide_39, guide_38)

guide_40 = Guide_gravity(
    name="Guide_40",
    w1=0.070052,
    h1=0.083340,
    w2=0.068891,
    h2=0.081295,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=132.000000,
    z2=136.000000,
)
chain_guide_straight(guide_40, guide_39)

guide_41 = Guide_gravity(
    name="Guide_41",
    w1=0.068891,
    h1=0.081295,
    w2=0.066734,
    h2=0.078364,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=2.5,
    mbottom=2.5,
    z1=136.000000,
    z2=140.000000,
)
chain_guide_straight(guide_41, guide_40)

guide_42 = Guide_gravity(
    name="Guide_42",
    w1=0.066734,
    h1=0.078364,
    w2=0.063480,
    h2=0.074442,
    l=4.000000,
    mleft=1,
    mright=1,
    mtop=3,
    mbottom=3,
    z1=140.000000,
    z2=144.000000,
)
chain_guide_straight(guide_42, guide_41)

guide_43 = Guide_gravity(
    name="Guide_43",
    w1=0.063480,
    h1=0.074442,
    w2=0.058948,
    h2=0.069361,
    l=4.000000,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=144.000000,
    z2=148.000000,
)
chain_guide_straight(guide_43, guide_42)

guide_44 = Guide_gravity(
    name="Guide_44",
    w1=0.058948,
    h1=0.069361,
    w2=0.053665,
    h2=0.063733,
    l=3.509000,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=148.000000,
    z2=151.509000,
)
chain_guide_straight(guide_44, guide_43)

# Gap 44->45 holds the FAN Chopper (ToO: "FAN Chopper (pos.: 151552,47 mm)").
guide_45 = Guide_gravity(
    name="Guide_45",
    w1=0.053665,
    h1=0.063733,
    w2=0.045385,
    h2=0.055335,
    l=4.000000,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=151.596000,
    z2=155.596000,
)
chain_guide_straight(guide_45, guide_44)

# Guide 46 does not exist in Table of Optics V3.2 - the numbering goes
# straight from 45 to 47.
guide_47 = Guide_gravity(
    name="Guide_47",
    w1=0.045385,
    h1=0.055335,
    w2=0.038918,
    h2=0.049103,
    l=2.399000,
    mleft=2,
    mright=2,
    mtop=4,
    mbottom=4,
    z1=155.596000,
    z2=157.995000,
)
chain_guide_straight(guide_47, guide_45)

# =============================================================================
# 48a/48b/48c occupy the same 1000 mm slot (158.000-159.000 m) as mutually
# exclusive polarizer options; only 48b (plain guide, no polarizer) is
# modelled here.
#   48a: SEOP 3He thermal polarizer - a 361 mm guide sits recessed inside the
#        cell (635.5 mm in from the slot's start, 3.5 mm short of its end).
#        Not added - removed pending a decision on the WHEN/instrument-
#        parameter wiring for the polarizer options.
#   48b: plain guide straight through the slot (no polarizer installed).
#   48c: solid-state V-cavity cold polarizer - not a Guide_gravity, and the
#        ToO gives it no aperture or m-index numbers, so it isn't modelled
#        here. Needs its own component once that's decided.
# =============================================================================

guide_48b = Guide_gravity(
    name="Guide_48B",
    w1=0.038918,
    h1=0.049103,
    w2=0.035667,
    h2=0.046092,
    l=1.000000,
    mleft=2,
    mright=2,
    mtop=4.5,
    mbottom=4.5,
    z1=158.000000,
    z2=159.000000,
)
chain_guide_straight(guide_48b, guide_47)

guide_49 = Guide_gravity(
    name="Guide_49",
    w1=0.035657,
    h1=0.046082,
    w2=0.022433,
    h2=0.034987,
    l=2.982000,
    mleft=2,
    mright=2,
    mtop=4.5,
    mbottom=4.5,
    z1=159.003000,
    z2=161.985000,
)
chain_guide_straight(guide_49, guide_48b)

# MC Gap: 95 mm slot for the M-Chopper (ToO: "M-Chopper (Pos.: 162m)"). A
# branch off Guide_49, same pattern as arm_psc above; Guide_50a still chains
# directly off Guide_49.
arm_mc = Arm(
    name="Arm_MC",
    l=0.095000,
    z1=161.985000,
    z2=162.080000,
)
chain_guide_straight(arm_mc, guide_49)

guide_50a = Guide_gravity(
    name="Guide_50A",
    w1=0.022433,
    h1=0.034987,
    w2=0.014184,
    h2=0.029556,
    l=1.003000,
    mleft=3.5,
    mright=3.5,
    mtop=4.5,
    mbottom=4.5,
    z1=162.083000,
    z2=163.086000,
)
chain_guide_straight(guide_50a, arm_mc)

# 50b/50c ("honeycomb collimator 1/2") share Guide_50a's 1003 mm span in the
# ToO, but it gives them no width/height/m-index - matches this project's own
# changelog note that the honeycomb collimators have "not correct parameters
# for now". They need a dedicated collimator component, not Guide_gravity;
# not added here.

# =============================================================================
# Straight guides (post-curve)
# =============================================================================
guides_straight_1 = [
    guide_30,
    guide_31,
    guide_32,
    arm_psc,
]

guides_straight_2 = [
    guide_33,
    guide_34,
    guide_35,
    guide_36,
    guide_37,
    guide_38,
    guide_39,
    guide_40,
    guide_41,
    guide_42,
    guide_43,
    guide_44,
    guide_45,
    guide_47,
    guide_48b,
    guide_49,
    arm_mc,
]

guides_straight_3 = [
    guide_50a,
]
