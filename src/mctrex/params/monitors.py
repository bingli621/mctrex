from mctrex.mcstas_components import Monitor_nD
from mctrex.params.guides_curve import arm_bm1

bm1 = Monitor_nD(
    name="BM1",
    options="setBM1",
    xwidth=0.06,
    yheight=0.084,
    filename='"BM1_tof.dat"',
    restore_neutron=1,
)
bm1.AT = [0, 0, arm_bm1.l / 2]
bm1.RELATIVE = "arm_BM1"
