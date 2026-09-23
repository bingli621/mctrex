import numpy as np

from mctrex.mcstas_components import Arm, Guide_gravity, curve_rot_y, gap
from mctrex.params.guides_extraction import arm_NBOA

# =============================================================================
# Common exit plane of the section-4 assembly at 5881.65 mm.
# Anchored to Guide_3 rather than Guide_4a so it is branch-independent:
# 4a and 4b share this plane, and 4b's exit tangent is on-axis.
#
# The -x wall releases at 5.927 m; from Guide_5 onward the guide is
# symmetric about its own axis again, so the tilt is removed there.
# =============================================================================

arm_after_bender = Arm(name="arm_after_bender")
arm_after_bender.AT = [0, 0, arm_NBOA.z2 - arm_NBOA.AT[2]]
arm_after_bender.RELATIVE = "arm_NBOA"


curve_radius = 12_000  # [m]


def chain_guide_curve(current, previous):
    """Place `guide` right after `previous` on the curve; mutates and returns `guide`."""
    g = gap(previous, current)
    current.AT = [0, 0, previous.l + g]
    current.ROTATED = [0, curve_rot_y(previous, g, current, curve_radius), 0]
    current.RELATIVE = previous.name
    return current


guide_5 = Guide_gravity(
    name="Guide_5",
    w1=0.06,
    h1=0.04626,
    w2=0.06,
    h2=0.05398,
    l=2.7625,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    z1=5.916,
    z2=8.6785,
)

_rot_y = -arm_NBOA.ROTATED[1] + np.degrees(guide_5.l / 2 / curve_radius)

guide_5.AT = [0, 0, guide_5.z1 - arm_NBOA.z2]
guide_5.ROTATED = [0, _rot_y, 0]
guide_5.RELATIVE = "arm_after_bender"


# =============================================================================
# 12km radius of curvature starts from this section of T-REX!
# =============================================================================

guide_6 = Guide_gravity(
    name="Guide_6",
    w1=0.060000,
    h1=0.054015,
    w2=0.060000,
    h2=0.060228,
    l=2.762500,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=8.69150,
    z2=11.454,
)
chain_guide_curve(guide_6, guide_5)

# =============================================================================
guide_7 = Guide_gravity(
    name="Guide_7",
    w1=0.060000,
    h1=0.060255,
    w2=0.060000,
    h2=0.067416,
    l=4.000000,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=11.467,
    z2=15.467,
)
chain_guide_curve(guide_7, guide_6)

# =============================================================================
guide_8 = Guide_gravity(
    name="Guide_8",
    w1=0.060000,
    h1=0.067419,
    w2=0.060000,
    h2=0.072976,
    l=4.000000,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=15.469,
    z2=19.469,
)
chain_guide_curve(guide_8, guide_7)

# =============================================================================
guide_9 = Guide_gravity(
    name="Guide_9",
    w1=0.060000,
    h1=0.072979,
    w2=0.060000,
    h2=0.076525,
    l=3.216700,
    mleft=1.5,
    mright=1.5,
    mtop=3,
    mbottom=3,
    z1=19.471,
    z2=22.6877,
)
chain_guide_curve(guide_9, guide_8)

# =============================================================================
guide_10 = Guide_gravity(
    name="Guide_10",
    w1=0.060000,
    h1=0.076538,
    w2=0.060000,
    h2=0.078024,
    l=1.588000,
    mleft=2,
    mright=2,
    mtop=2.5,
    mbottom=2.5,
    z1=22.7007,
    z2=24.2887,
)
chain_guide_curve(guide_10, guide_9)

# =============================================================================
guide_11 = Guide_gravity(
    name="Guide_11",
    w1=0.060000,
    h1=0.078035,
    w2=0.060000,
    h2=0.080842,
    l=3.634900,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=24.3017,
    z2=27.9366,
)
chain_guide_curve(guide_11, guide_10)

# =============================================================================
guide_12 = Guide_gravity(
    name="Guide_12",
    w1=0.060000,
    h1=0.080848,
    w2=0.060000,
    h2=0.082063,
    l=1.999800,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=27.94614,
    z2=29.94594,
)
chain_guide_curve(guide_12, guide_11)

# =============================================================================
guide_13a = Guide_gravity(
    name="Guide_13A",
    w1=0.060000,
    h1=0.082065,
    w2=0.060000,
    h2=0.083061,
    l=1.999800,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=29.94924,
    z2=31.94904,
)
chain_guide_curve(guide_13a, guide_12)

# 13A Pre BWC1
# =============================================================================
guide_13b = Guide_gravity(
    name="Guide_13B",
    w1=0.060000,
    h1=0.083074,
    w2=0.060000,
    h2=0.083856,
    l=1.999800,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=31.97904,
    z2=33.97884,
)
chain_guide_curve(guide_13b, guide_13a)

# 13B Post BWC1
# =============================================================================
guide_14a = Guide_gravity(
    name="Guide_14A",
    w1=0.060000,
    h1=0.083857,
    w2=0.060000,
    h2=0.084433,
    l=1.999800,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=33.98214,
    z2=35.98194,
)
chain_guide_curve(guide_14a, guide_13b)

# =============================================================================
guide_14b = Guide_gravity(
    name="Guide_14B",
    w1=0.060000,
    h1=0.084433,
    w2=0.060000,
    h2=0.084803,
    l=1.963300,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=35.98264,
    z2=37.94594,
)
chain_guide_curve(guide_14b, guide_14a)

# 15A Pre BWC2
# =============================================================================
guide_15a = Guide_gravity(
    name="Guide_15A",
    w1=0.060000,
    h1=0.084803,
    w2=0.060000,
    h2=0.084983,
    l=1.990800,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=37.94925,
    z2=39.94004,
)
chain_guide_curve(guide_15a, guide_14b)

# 15B Post BWC2
# =============================================================================
guide_15b = Guide_gravity(
    name="Guide_15B",
    w1=0.060000,
    h1=0.084984,
    w2=0.060000,
    h2=0.084965,
    l=2.001200,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=39.97004,
    z2=41.97124,
)
chain_guide_curve(guide_15b, guide_15a)
# =============================================================================

arm_bm1 = Arm(
    name="arm_BM1",
    l=0.02,
    z1=41.97786,
    z2=41.99786,
)
chain_guide_curve(arm_bm1, guide_15b)

# =============================================================================
guide_16 = Guide_gravity(
    name="Guide_16",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=42.00155,
    z2=45.99825,
)
chain_guide_curve(guide_16, guide_15b)

# =============================================================================
guide_17 = Guide_gravity(
    name="Guide_17",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=46.00155,
    z2=49.99825,
)
chain_guide_curve(guide_17, guide_16)

# =============================================================================
guide_18 = Guide_gravity(
    name="Guide_18",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=50.00155,
    z2=53.99825,
)
chain_guide_curve(guide_18, guide_17)

# =============================================================================
guide_19 = Guide_gravity(
    name="Guide_19",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=54.00155,
    z2=57.99825,
)
chain_guide_curve(guide_19, guide_18)

# =============================================================================
guide_20 = Guide_gravity(
    name="Guide_20",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=58.00155,
    z2=61.99825,
)
chain_guide_curve(guide_20, guide_19)

# =============================================================================
guide_21 = Guide_gravity(
    name="Guide_21",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=62.00155,
    z2=65.99825,
)
chain_guide_curve(guide_21, guide_20)

# =============================================================================
guide_22 = Guide_gravity(
    name="Guide_22",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=66.00155,
    z2=69.99825,
)
chain_guide_curve(guide_22, guide_21)

# =============================================================================
guide_23 = Guide_gravity(
    name="Guide_23",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=70.00155,
    z2=73.99825,
)
chain_guide_curve(guide_23, guide_22)

# =============================================================================
guide_24 = Guide_gravity(
    name="Guide_24",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=74.00155,
    z2=77.99825,
)
chain_guide_curve(guide_24, guide_23)

# =============================================================================
guide_25 = Guide_gravity(
    name="Guide_25",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1.5,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=78.00155,
    z2=81.99825,
)
chain_guide_curve(guide_25, guide_24)

# =============================================================================
guide_26 = Guide_gravity(
    name="Guide_26",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=82.00155,
    z2=85.99825,
)
chain_guide_curve(guide_26, guide_25)

# =============================================================================
guide_27 = Guide_gravity(
    name="Guide_27",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=86.00155,
    z2=89.99825,
)
chain_guide_curve(guide_27, guide_26)

# =============================================================================
guide_28 = Guide_gravity(
    name="Guide_28",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=3.996700,
    mleft=1,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=90.00155,
    z2=93.99825,
)
chain_guide_curve(guide_28, guide_27)

# End of 12 km curve radius / end of T1 (96 m)
# =============================================================================
guide_29 = Guide_gravity(
    name="Guide_29",
    w1=0.060000,
    h1=0.085000,
    w2=0.060000,
    h2=0.085000,
    l=1.998000,
    mleft=1,
    mright=2.5,
    mtop=2.5,
    mbottom=2.5,
    z1=94.00155,
    z2=95.99955,
)
chain_guide_curve(guide_29, guide_28)

# =============================================================================
# Curved guides
# =============================================================================
guides_curve_1 = [
    arm_after_bender,
    guide_5,
    guide_6,
    guide_7,
    guide_8,
    guide_9,
    guide_10,
    guide_11,
    guide_12,
    guide_13a,
]

guides_curve_2 = [
    guide_13b,
    guide_14a,
    guide_14b,
    guide_15a,
]

guides_curve_3 = [
    guide_15b,
    arm_bm1,
]

guides_curve_4 = [
    guide_16,
    guide_17,
    guide_18,
    guide_19,
    guide_20,
    guide_21,
    guide_22,
    guide_23,
    guide_24,
    guide_25,
    guide_26,
    guide_27,
    guide_28,
    guide_29,
]
