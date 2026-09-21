import numpy as np

from mctrex.mcstas_components import (
    Arm,
    Guide_gravity,
    Pol_bender,
)

# =============================================================================
# NBOA (Neutron Beam Optics Assembly), guide_1 -> guide_3
# =============================================================================
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
# NBOA taper angle: half the 0.426695 deg ToO horizontal taper angle,
# computed from the fixed -x wall and the Guide_1/Guide_4b entrance-to-exit
# geometry above (see the NBOA notes above arm_NBOA).
# =============================================================================

# ---------------- NBOA - ASYMMETRIC TAPER ----------------
# Note: _entrance_x = -0.002 because guide is asymmetric here ((47mm-43mm)/2

_width_entrance, _width_exit = 0.089955, 0.060256  # [m]
_z_entrance, _z_exit = 1.89593, 5.88165  # [m]
_taper_angle = np.degrees(
    np.arctan((_width_entrance - _width_exit) / (_z_exit - _z_entrance) / 2)
)
_fixed_wall_at = -0.047  # [m]
_x_entrance = _width_entrance * np.cos(np.radians(_taper_angle)) / 2 + _fixed_wall_at

arm_NBOA = Arm(name="arm_NBOA", z1=_z_entrance, z2=_z_exit)
arm_NBOA.AT = [_x_entrance, 0, _z_entrance]
arm_NBOA.ROTATED = [0, -_taper_angle, 0]

# Guide_gravity is symmetric about its own axis, but two straight walls are
# reproduced EXACTLY by a symmetric guide placed on their bisector. The
# tilt is identical for all four sections, so one arm carries the whole
# NBOA and the sections hang off it with plain z offsets.

guide_1 = Guide_gravity(
    name="Guide_1",
    w1=0.089955,  # _width_entrance = 0.089955
    h1=0.029992,
    w2=0.082455,
    h2=0.034937,
    l=0.9994,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    z1=1.89593,  # _z_entrance = 1.89593
    z2=2.89533,
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
    z1=2.89633,  # 1.0 mm gap after Guide_1
    z2=3.89553,
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
    z1=3.89673,  # 1.2 mm gap after Guide_2
    z2=5.37593,
)
guide_3.AT = [0, 0, guide_3.z1 - guide_1.z1]
guide_3.RELATIVE = "arm_NBOA"

# =============================================================================
# BBGOA (Beam Bridge Guide Optics Assembly)
# EXCHANGE ASSEMBLY (4a thermal <-> 4b cold + bender)
# =============================================================================
#
# 4a and 4b occupy the same slot in the BBGOA and share the same exit plane
# at 5881.65 mm; they are alternative optics that swap in and out, NOT
# parallel beamlines. Both are anchored to Guide_3 so the two WHEN branches
# are fully independent of each other.
#
# Ref: ToO v3.0
#
# ---- 4a: thermal guide | 5400.65 -> 5881.65 mm | 481 mm | Aluminium ----
# =============================================================================

guide_4a = Guide_gravity(
    name="Guide_4a",
    w1=0.063838,
    h1=0.04459,
    w2=0.06026,  # _width_exit = 0.060256
    h2=0.04615,
    l=0.481,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    z1=5.40065,
    z2=5.88165,  # _z_exit = 5.88165
)
guide_4a.AT = [0, 0, guide_4a.z1 - guide_1.z1]
guide_4a.RELATIVE = "arm_NBOA"
guide_4a.WHEN = "bender==0"

# =============================================================================
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
# note: radius > 0 curves left (+x).
# =============================================================================
# mirror_params
# R0, Low-angle reflectivity
# Qc, Critical scattering vector
# alpha, Slope of reflectivity
# m, m-value of material. Zero means completely absorbing.
# W, Width of supermirror cut-off for all mirrors
mirror_params = (0.99, 0.0219, 3.02, 4.0, 0.003)
mirror_params_str = f"{{{','.join(map(str, mirror_params))}}}"
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
    G=0,  # default is 9.8
    # match G=0 used by every Guide_gravity;
    # comp default is 9.8 and its gravity path
    # is flagged untested in the component BUGS
    # All four walls set explicitly: the component description says Bot/Left/
    # Right inherit from Top, but the parameter table lists an independent
    # m=2 default for each. Explicit values settle the ambiguity.
    # Identical Up/Down arrays make the component spin-independent.
    rTopUpPar=mirror_params_str,
    rTopDownPar=mirror_params_str,
    rBotUpPar=mirror_params_str,
    rBotDownPar=mirror_params_str,
    rLeftUpPar=mirror_params_str,
    rLeftDownPar=mirror_params_str,
    rRightUpPar=mirror_params_str,
    rRightDownPar=mirror_params_str,
)
pol_bender.AT = guide_4a.AT
pol_bender.RELATIVE = "arm_NBOA"
pol_bender.WHEN = "bender==1"
# ROTATED is left unset: it's [0, b_rot, 0], and b_rot is an instrument
# parameter that only exists once the notebook creates it.

guide_4b = Guide_gravity(
    name="Guide_4b",
    w1=0.063466,
    h1=0.044759,
    w2=0.060256,  # _width_exit = 0.060256
    h2=0.046152,
    l=0.431,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    z1=5.45065,
    z2=5.88165,  # _z_exit = 5.88165
)
guide_4b.AT = [0, 0, guide_4b.z1 - guide_1.z1]
guide_4b.RELATIVE = "arm_NBOA"
guide_4b.WHEN = "bender==1"

# =============================================================================
# Bispectral extraction guides
# =============================================================================

guides_extraction = [
    arm_NBOA,
    guide_1,
    guide_2,
    guide_3,
    guide_4a,
    pol_bender,
    guide_4b,
]
