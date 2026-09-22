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
_gap = gap(guide_6, guide_5)
_rot_y = curve_rot_y(guide_5, guide_6, _gap)

guide_6.AT = [0, 0, guide_5.l + _gap]
guide_6.ROTATED = [0, _rot_y, 0]
guide_6.RELATIVE = "Guide_5"


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
_gap = gap(guide_7, guide_6)
_rot_y = curve_rot_y(guide_6, guide_7, _gap)

guide_7.AT = [0, 0, guide_6.l + _gap]
guide_7.ROTATED = [0, _rot_y, 0]
guide_7.RELATIVE = "Guide_6"

# AT (0, 0, 2.762500+13e-3) RELATIVE Guide_6
# ROTATED (0, (3.394250/12000)*RAD2DEG, 0) RELATIVE Guide_6

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
_gap = gap(guide_8, guide_7)
_rot_y = curve_rot_y(guide_7, guide_8, _gap)

guide_8.AT = [0, 0, guide_7.l + _gap]
guide_8.ROTATED = [0, _rot_y, 0]
guide_8.RELATIVE = "Guide_7"

# AT (0, 0, 4+2e-3) RELATIVE Guide_7
# ROTATED (0, (4.002000/12000)*RAD2DEG, 0) RELATIVE Guide_7

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
_gap = gap(guide_9, guide_8)
_rot_y = curve_rot_y(guide_8, guide_9, _gap)

guide_9.AT = [0, 0, guide_8.l + _gap]
guide_9.ROTATED = [0, _rot_y, 0]
guide_9.RELATIVE = "Guide_8"

# AT (0, 0, 4+2e-3) RELATIVE Guide_8
# ROTATED (0, (3.610350/12000)*RAD2DEG, 0) RELATIVE Guide_8

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
_gap = gap(guide_10, guide_9)
_rot_y = curve_rot_y(guide_9, guide_10, _gap)

guide_10.AT = [0, 0, guide_9.l + _gap]
guide_10.ROTATED = [0, _rot_y, 0]
guide_10.RELATIVE = "Guide_9"

# AT (0, 0, 3.2167+13e-3) RELATIVE Guide_9
# ROTATED (0, (2.415350/12000)*RAD2DEG, 0) RELATIVE Guide_9

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
_gap = gap(guide_11, guide_10)
_rot_y = curve_rot_y(guide_10, guide_11, _gap)

guide_11.AT = [0, 0, guide_10.l + _gap]
guide_11.ROTATED = [0, _rot_y, 0]
guide_11.RELATIVE = "Guide_10"

# AT (0, 0, 1.588000+13e-3) RELATIVE Guide_10
# ROTATED (0, (2.624450/12000)*RAD2DEG, 0) RELATIVE Guide_10

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
_gap = gap(guide_12, guide_11)
_rot_y = curve_rot_y(guide_11, guide_12, _gap)

guide_12.AT = [0, 0, guide_11.l + _gap]
guide_12.ROTATED = [0, _rot_y, 0]
guide_12.RELATIVE = "Guide_11"

# AT (0, 0, 3.634900+9.54e-3) RELATIVE Guide_11
# ROTATED (0, (2.826890/12000)*RAD2DEG, 0) RELATIVE Guide_11

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
_gap = gap(guide_13a, guide_12)
_rot_y = curve_rot_y(guide_12, guide_13a, _gap)

guide_13a.AT = [0, 0, guide_12.l + _gap]
guide_13a.ROTATED = [0, _rot_y, 0]
guide_13a.RELATIVE = "Guide_12"

# //13A Pre BWC1
# AT (0, 0, 1.999800+3.3e-3) RELATIVE Guide_12
# ROTATED (0, (2.003100/12000)*RAD2DEG, 0) RELATIVE Guide_12


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
_gap = gap(guide_13b, guide_13a)
_rot_y = curve_rot_y(guide_13a, guide_13b, _gap)

guide_13b.AT = [0, 0, guide_13a.l + _gap]
guide_13b.ROTATED = [0, _rot_y, 0]
guide_13b.RELATIVE = "Guide_13A"

# //13B Post BWC1
# AT (0, 0, 15e-3) RELATIVE BW_Chopper_1
# ROTATED (0, (2.029800/12000)*RAD2DEG, 0) RELATIVE BW_Chopper_1

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
]
