from mctrex.mcstas_components import NXdisk_chopper
from mctrex.params.guides_curve import arm_bwc1, arm_bwc2
from mctrex.params.guides_straight import arm_mc, arm_psc

bw1 = NXdisk_chopper(
    name="BW_Chopper_1",
    slit_edges=(-30.7, 30.7),
    n_edges=2,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=0,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

bw1.AT = [0, 0, arm_bwc1.l / 2]
bw1.RELATIVE = "Arm_BWC1"


bw2 = NXdisk_chopper(
    name="BW_Chopper_2",
    slit_edges=(-31.65, 31.65),
    n_edges=2,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=0,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

bw2.AT = [0, 0, arm_bwc2.l / 2]
bw2.RELATIVE = "Arm_BWC2"

ps1 = NXdisk_chopper(
    name="PS_Chopper_1",
    slit_edges=(-10, 10, 107.5, 142.5, 170, 190, 287.5, 322.5),
    n_edges=8,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=180,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

ps1.AT = [0, 0, arm_psc.l / 2 - 0.05]
ps1.RELATIVE = "Arm_PSC"

ps2 = NXdisk_chopper(
    name="PS_Chopper_2",
    slit_edges=(-10, 10, 107.5, 142.5, 170, 190, 287.5, 322.5),
    n_edges=8,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=180,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

ps2.AT = [0, 0, arm_psc.l / 2 + 0.05]
ps2.RELATIVE = "Arm_PSC"


mc1 = NXdisk_chopper(
    name="MC_Chopper_1",
    slit_edges=(178.25, 181.25, 362.8, 367.2),
    n_edges=4,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=180,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

mc1.AT = [0, 0, arm_mc.l / 2 - 0.005]
mc1.RELATIVE = "Arm_MC"

mc2 = NXdisk_chopper(
    name="MC_Chopper_2",
    slit_edges=(-1.25, 1.25, 182.8, 187.2),
    n_edges=4,
    radius=0.35,
    yheight=0.08,
    xwidth=0.0,  # 0.06
    beam_angle=0,
    zero_angle=0,
    abs_out=0,
    verbose=1,
)

mc2.AT = [0, 0, arm_mc.l / 2 + 0.005]
mc2.RELATIVE = "Arm_MC"
