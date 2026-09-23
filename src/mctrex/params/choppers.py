from mctrex.mcstas_components import NXdisk_chopper, gap
from mctrex.params.guides_curve import (
    guide_13a,
    guide_13b,
    guide_15a,
    guide_15b,
)

bw1 = NXdisk_chopper(
    name="BW_Chopper_1",
    slit_edges="{-30.7, 30.7}",
    n_edges=2,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=0,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

bw1.AT = [0, 0, guide_13a.l + gap(guide_13a, guide_13b) / 2]
bw1.RELATIVE = "Guide_13A"


bw2 = NXdisk_chopper(
    name="BW_Chopper_2",
    slit_edges="{-31.65, 31.65}",
    n_edges=2,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=0,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

bw2.AT = [0, 0, guide_15a.l + gap(guide_15a, guide_15b) / 2]
bw2.RELATIVE = "Guide_15A"
