from mctrex.mcstas_components import ESS_butterfly, Progress_bar

# =============================================================================
# ORIGIN
# =============================================================================

origin = Progress_bar(name="origin", percent=10)

# =============================================================================
# ESS SOURCE
# =============================================================================

source = ESS_butterfly(
    name="source",
    sector='"W"',
    beamline=7,
    # Lmin=0.1,   # in Angstrom
    # Lmax=10.0,  # in Angstrom
    acc_power=2,  # [MW]
    yheight=0.03,  # [m], moderator height, 0.03 to 0.06
    cold_frac=0.3,
    dist=2,  # [m], distance to focusing rectangle
    focus_xw=0.095,  # [m], size of focusing rectangle
    focus_yh=0.035,
    n_pulses=1,
)
