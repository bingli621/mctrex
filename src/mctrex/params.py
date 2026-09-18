"""
Component parameters for the ESS_butterfly_W7 instrument.
"""

import numpy as np

from mctrex.mcstas_components import Arm, ESS_butterfly, Guide_gravity, Pol_bender

source = ESS_butterfly(
    name="source",
    sector='"W"',
    beamline=7,
    Lmin=0.1,  # in Angstrom
    Lmax=10.0,  # in Angstrom
    acc_power=2,  # [MW]
    yheight=0.03,  # [m], moderator height, 0.03 to 0.06
    cold_frac=0.3,
    dist=2,  # [m], distance to focusing rectange
    focus_xw=0.095,  # [m], size of focusing rectange
    focus_yh=0.035,
    n_pulses=1,
)

# NBOA (Neutron Beam Optics Assembly), guide_1 -> guide_4a/4b
#
# NBOA - ASYMMETRIC TAPER
#
# The -x wall of the NBOA is FIXED at -47.000 mm; all of the horizontal
# narrowing (90 -> 60 mm) is taken out of the +x wall, which is the cold
# moderator side. This is the bispectral extraction geometry: the view of
# the thermal face is held constant while the cold-side acceptance is
# trimmed.
#
# Consequence: the guide centre-line is NOT the nominal beam axis. It is a
# straight line from -2.0295 mm at 1895.927 mm to -16.8711 mm at 5881.65 mm,
# tilted by -0.213350 deg = half the 0.426695 deg ToO horizontal taper
# angle.
#
# Guide_gravity is symmetric about its own axis, but two straight walls are
# reproduced EXACTLY by a symmetric guide placed on their bisector. The
# tilt is identical for all four sections, so one arm carries the whole
# NBOA and the sections hang off it with plain z offsets.
#
# The -x wall releases at 5.927 m; from Guide_5 onward the guide is
# symmetric about its own axis again, so the tilt is removed there.
arm_NBOA = Arm(name="arm_NBOA")

guide_1 = Guide_gravity(
    name="Guide_1",
    w1=0.089955,
    h1=0.029992,
    w2=0.082455,
    h2=0.034937,
    l=0.9994,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    z1=1.89593,
    z2=2.89533,
    # comment="/* 1895.93 -> 2895.33 mm */",
)
guide_1.AT = [0, 0, 0]
guide_1.RELATIVE = "arm_NBOA"

guide_2 = Guide_gravity(
    name="Guide_2",
    w1=0.082447,
    h1=0.034941,
    w2=0.074948,
    h2=0.03916,
    l=0.9992,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    z1=2.89633,
    z2=3.89553,
    # comment="/* 2896.33 -> 3895.53 mm */",
)
guide_2.AT = [0, 0, guide_2.z1 - guide_1.z1]
guide_2.RELATIVE = "arm_NBOA"

guide_3 = Guide_gravity(
    name="Guide_3",
    w1=0.074939,
    h1=0.039164,
    w2=0.063838,
    h2=0.044511,
    l=1.47920,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    z1=3.89673,
    z2=5.37593,
    # comment="/* 3896.73 -> 5375.93 mm */",
)
guide_3.AT = [0, 0, guide_3.z1 - guide_1.z1]
guide_3.RELATIVE = "arm_NBOA"

# BBGOA (Beam Bridge Guide Optics Assembly)
#
# BBGOA SECTION 4 - EXCHANGE ASSEMBLY (4a thermal <-> 4b cold + bender)
#
# 4a and 4b occupy the same slot in the BBGOA and share the same exit plane
# at 5881.65 mm; they are alternative optics that swap in and out, NOT
# parallel beamlines. Both are anchored to Guide_3 so the two WHEN branches
# are fully independent of each other.
#
# Ref: ToO v3.2
#
# ---- 4a: thermal guide | 5400.65 -> 5881.65 mm | 481 mm | Aluminium ----
guide_4a = Guide_gravity(
    name="Guide_4a",
    w1=0.063838,
    h1=0.04459,
    w2=0.06026,
    h2=0.04615,
    l=0.481,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    z1=5.40065,
    z2=5.88165,
    # comment="/* 5400.65 -> 5881.65 mm */",
)
guide_4a.AT = [0, 0, guide_4a.z1 - guide_1.z1]
guide_4a.WHEN = "bender==0"
guide_4a.RELATIVE = "arm_NBOA"


# NBOA taper angle: half the 0.426695 deg ToO horizontal taper angle,
# computed from the fixed -x wall and the Guide_1/Guide_4b entrance-to-exit
# geometry above (see the NBOA notes above arm_NBOA).
_taper_angle = np.degrees(
    np.arctan((guide_1.w1 - guide_4a.w2) / (guide_4a.z2 - guide_1.z1) / 2)
)
_fixed_wall_at = -0.047  # m
arm_NBOA.AT = [
    guide_1.w1 * np.cos(np.radians(_taper_angle)) / 2 + _fixed_wall_at,
    0,
    guide_1.z1,
]
arm_NBOA.ROTATED = [0, -_taper_angle, 0]


# ---- 4b: bender + cold guide | 5400 -> 5450.65 -> 5881.65 mm | 50 + 431 mm | Aluminium
#
# The bender is a 50 mm solid-state Si stack at the UPSTREAM end of 4b
# (5400.65 -> 5450.65 mm), followed by 381 mm of tapered cold guide
# (5450.65 -> 5881.65 mm). Every Si channel is 0.15 mm wide, sputtered on
# every side with Ni/Ti m=4, blade radius of curvature 7.2 m -> deflection
# = atan(0.05/7.2) = 0.3979 deg. The entrance is oriented toward the cold
# moderator; the exit tangent lies on the nominal guide axis, so nothing
# downstream of 4b is rotated.
#
# NOTE: radius > 0 curves left (+x).
pol_bender = Pol_bender(
    name="bender",
    xwidth=0.063466,
    yheight=0.044759,
    length=0.050,
    radius=7.2,
    nslit=426,
    d=1e-6,
    endFlat=0,
    drawOption=2,
    # match G=0 used by every Guide_gravity;
    # comp default is 9.8 and its gravity path
    # is flagged untested in the component BUGS
    # All four walls set explicitly: the component description says Bot/Left/
    # Right inherit from Top, but the parameter table lists an independent
    # m=2 default for each. Explicit values settle the ambiguity.
    # Identical Up/Down arrays make the component spin-independent.
    rTopUpPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rTopDownPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rBotUpPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rBotDownPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rLeftUpPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rLeftDownPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rRightUpPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
    rRightDownPar="{0.99, 0.0219, 3.02, 4.0, 0.003}",
)
pol_bender.AT = guide_4a.AT
pol_bender.WHEN = "bender==1"
pol_bender.RELATIVE = "arm_NBOA"
# ROTATED is left unset: it's [0, b_rot, 0], and b_rot is an instrument
# parameter that only exists once the notebook creates it.

guide_4b = Guide_gravity(
    name="Guide_4b",
    w1=0.063466,
    h1=0.044759,
    w2=0.060256,
    h2=0.046152,
    l=0.431,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    z1=5.45065,
    z2=5.88165,
    # comment="/* 5450.65 -> 5881.65 mm */",
)
guide_4b.AT = [0, 0, guide_4b.z1 - guide_1.z1]
guide_4b.WHEN = "bender==1"
guide_4b.RELATIVE = "arm_NBOA"


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
    # comment="/* 5916.00 -> 8678.50 mm */",
)
guide_5.AT = [0, 0, 34.35e-3]
guide_5.ROTATED = [0, 0.213350 + 0.006595, 0]
guide_5.RELATIVE = "arm_after_bender"


# Common exit plane of the section-4 assembly at 5881.65 mm.
# Anchored to Guide_3 rather than Guide_4a so it is branch-independent:
# 4a and 4b share this plane, and 4b's exit tangent is on-axis.
arm_after_bender = Arm(name="arm_after_bender")
arm_after_bender.AT = [0, 0, 3.985723]
arm_after_bender.RELATIVE = "arm_NBOA"

# Instrument order: each RELATIVE target must be added before whatever
# references it (arm_after_bender before guide_5, arm_NBOA before everything
# else that references it).
components = [
    source,
    arm_NBOA,
    guide_1,
    guide_2,
    guide_3,
    guide_4a,
    pol_bender,
    guide_4b,
    arm_after_bender,
    guide_5,
]
