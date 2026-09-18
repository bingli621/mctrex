"""
Dataclass wrappers for McStasScript components.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


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


def add_components_to(instrument, components):
    """Add every component in `components` to `instrument`.

    Returns a dict mapping each component's name to the McStasScript
    component `add_to` created, so callers can keep operating on them
    (e.g. `.set_comment(...)`) after the batch add.
    """
    return {c.name: c.add_to(instrument) for c in components}


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


@dataclass(kw_only=True)
class ESS_butterfly(McStasComponent):
    """ESS butterfly moderator source."""

    sector: str  # quoted sector letter, e.g. '"W"'
    beamline: int
    Lmin: float  # [Angstrom]
    Lmax: float  # [Angstrom]
    acc_power: float  # [MW]
    yheight: float  # [m], moderator height, 0.03 to 0.06
    cold_frac: Any  # fraction of events emitted from the cold moderator
    dist: float  # [m], distance to focusing rectangle
    focus_xw: float  # [m], focusing rectangle width
    focus_yh: float  # [m], focusing rectangle height
    n_pulses: float = 1


@dataclass(kw_only=True)
class Pol_bender(McStasComponent):
    """Polarizing Si-stack bender segment."""

    xwidth: float  # [m], width at the guide entry
    yheight: float  # [m], height at the guide entry
    length: float  # [m], length of guide along center
    radius: float  # [m], radius of curvature (+ curves left/+x)
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
