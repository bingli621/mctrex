"""
Dataclass wrappers for McStasScript components.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np


def add_components_to(instrument, component_dict):
    """Add every component in `components` to `instrument`."""

    for component in component_dict.values():
        if isinstance(component, NXdisk_chopper):
            size = len(component.slit_edges)
            values = ", ".join(str(v) for v in component.slit_edges)
            instrument.append_declare(
                f"double slit_edges_{component.name}[{size}] = {{{values}}};"
            )
            component.slit_edges = f"slit_edges_{component.name}"
        component.add_to(instrument)
    return instrument


def gap(upstream, downstream):
    """Free space between `upstream`'s exit and `downstream`'s entrance."""

    return downstream.z1 - upstream.z2


def curve_rot_y(upstream, gap, downstream, curve_radius=12_000):
    """Midpoint-rule tilt increment [deg] from `upstream` to `downstream` on the `curve_radius` arc."""

    return np.degrees(((upstream.l + downstream.l) / 2 + gap) / curve_radius)


@dataclass(kw_only=True)
class McStasComponent:
    """Base for a McStasScript component: name + placement."""

    name: str
    AT: Sequence[float] = (0, 0, 0)
    ROTATED: Sequence[float] = (0, 0, 0)
    RELATIVE: Any = "ABSOLUTE"  # arm/component object (or name) relative to
    WHEN: str | None = None  # logical c expression component is conditional on

    _not_params = ("name", "AT", "ROTATED", "RELATIVE", "WHEN")

    def add_to(self, instrument, **extra_params):
        """Add this component to `instrument`, set its params, and return it."""
        comp = instrument.add_component(
            name=self.name,
            component_name=type(self).__name__,
            AT=list(self.AT),
            ROTATED=list(self.ROTATED),
            RELATIVE=self.RELATIVE,
            WHEN=self.WHEN,
        )
        params = {k: v for k, v in vars(self).items() if k not in self._not_params}
        comp.set_parameters(**params, **extra_params)
        return comp


@dataclass(kw_only=True)
class Progress_bar(McStasComponent):
    percent: float = 10


@dataclass(kw_only=True)
class ESS_butterfly(McStasComponent):
    """ESS butterfly moderator source."""

    sector: str  # quoted sector letter, e.g. '"W"'
    beamline: int

    acc_power: float  # [MW]
    yheight: float  # [m], moderator height, 0.03 to 0.06
    cold_frac: Any  # fraction of events emitted from the cold moderator
    dist: float  # [m], distance to focusing rectangle
    focus_xw: float  # [m], focusing rectangle width
    focus_yh: float  # [m], focusing rectangle height
    n_pulses: float = 1
    Lmin: float = 0.1  # [Angstrom]
    Lmax: float = 10.0  # [Angstrom]


@dataclass(kw_only=True)
class Guide_gravity(McStasComponent):
    """One Guide_gravity segment."""

    l: float  # length [m]
    w1: float  # entrance width [m]
    h1: float  # entrance height [m]
    w2: float  # exit width [m]
    h2: float  # exit height [m]
    mleft: float = -1
    mright: float = -1
    mtop: float = -1
    mbottom: float = -1

    z1: float  # z position of entrance [m]
    z2: float  # z position of exit [m]
    _not_params = McStasComponent._not_params + ("z1", "z2")


@dataclass(kw_only=True)
class Arm(McStasComponent):
    """A reference point/frame with no parameters of its own."""

    l: float = 0  # zero physical length, so it chains like any other guide joint
    z1: float = 0  # z position of entrance [m]
    z2: float = 0  # z position of exit [m]
    _not_params = McStasComponent._not_params + ("l", "z1", "z2")


@dataclass(kw_only=True)
class Monitor_nD(McStasComponent):
    """Generic McStas monitor; geometry from xwidth/yheight, behavior from `options`."""

    xwidth: float  # [m]
    yheight: float  # [m]
    # McStas "options" string written verbatim, so quoting is on the caller:
    # a literal spec needs embedded quotes (e.g. '"x limits [-0.15:0.15] bins=301"'),
    # while an unquoted name (e.g. "setBW2") references a DECLARE'd C string instead
    options: str
    filename: str  # quoted output filename, e.g. '"BW2_monitor_tof.dat"'
    restore_neutron: int = 1


@dataclass(kw_only=True)
class NXdisk_chopper(McStasComponent):
    """Disk chopper with an arbitrary number of slits, defined by slit edge angles."""

    # a plain sequence of values until add_components_to() DECLAREs it as a
    # named C array and rewrites this to that array's name (a str) instead
    slit_edges: Sequence[float] | str
    n_edges: int  # number of entries in slit_edges; must be even and non-zero

    radius: float = 0.35  # [m], outer radius of the disc
    yheight: float = 0  # [m], radial clearance of the openings; 0 reach the spindle
    xwidth: float = 0  # [m], chord width of the beam window; 0 for unrestricted opening
    nu: int = 14  # [Hz], signed rotation frequency; 0 parks the disc at park_angle
    delay: float = 0  # [s], when the disc's zero mark is on the beam
    park_angle: float = 0  # [deg],  only read when nu is 0
    beam_angle: float = 0  # [deg], where the beam crosses the disc, from the zero mark; 0 puts the beam at the top
    zero_angle: float = 0  # [deg], from the component's +y axis to the TDC pickup
    jitter: float = 0  # [s], timing jitter applied to each ray
    abs_out: int = 0  # absorb rays that miss the disc entirely
    verbose: int = 0  # -1: silent, 0: errors, 1: warnings, 2: info, 3: details


@dataclass(kw_only=True)
class Pol_bender(McStasComponent):
    """Polarizing Si-stack bender segment."""

    xwidth: float  # [m], width at the guide entry
    yheight: float  # [m], height at the guide entry
    length: float  # [m], length of guide along center
    radius: float  # [m], radius of curvature (+ curves left)
    nslit: int
    d: float  # [m], width of spacers
    endFlat: int
    drawOption: int
    # {maxR, Qc, alpha, m, W} reflectivity params, written verbatim as a C array
    # literal, hence the pre-formatted string rather than a Python sequence
    rTopUpPar: str
    rTopDownPar: str
    rBotUpPar: str
    rBotDownPar: str
    rLeftUpPar: str
    rLeftDownPar: str
    rRightUpPar: str
    rRightDownPar: str
    G: float = 9.8  # [m/s^2]
