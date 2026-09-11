"""
Dataclass wrapper for repeated Guide_gravity components in a McStasScript
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass
class GuideSection:
    """One Guide_gravity segment: geometry + placement + optional comment."""

    name: str
    l: float  # length [m]
    w1: float  # entrance width [m]
    h1: float  # entrance height [m]
    w2: float | None = None  # exit width [m]  (defaults to w1, i.e. straight guide)
    h2: float | None = None  # exit height [m] (defaults to h1)
    z1: float | None = None  # z position of entrance [m] (optional)
    z2: float | None = None  # z position of exit [m] (optional)
    mleft: float = -1
    mright: float = -1
    mtop: float = -1
    mbottom: float = -1

    AT: Sequence[float] = (0, 0, 0)
    ROTATED: Sequence[float] = (0, 0, 0)
    RELATIVE: Any = "ABSOLUTE"  # arm/component object (or name)relative to
    component_name: str = "Guide_gravity"

    def add_to(self, instrument):
        """Add this guide to `instrument` and return the created component."""
        comp = instrument.add_component(
            name=self.name,
            component_name=self.component_name,
            AT=list(self.AT),
            ROTATED=list(self.ROTATED),
            RELATIVE=self.RELATIVE,
        )
        comp.set_parameters(
            w1=self.w1,
            h1=self.h1,
            w2=self.w2 if self.w2 is not None else self.w1,
            h2=self.h2 if self.h2 is not None else self.h1,
            l=self.l,
            mleft=self.mleft,
            mright=self.mright,
            mtop=self.mtop,
            mbottom=self.mbottom,
        )
        return comp


guide_1 = GuideSection(
    name="Guide_1",
    w1=0.089955,
    h1=0.029992,
    w2=0.082455,
    h2=0.034937,
    l=0.9994,
    z1=1.89593,
    z2=2.89533,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    # comment="/* 1895.93 -> 2895.33 mm */",
)
guide_2 = GuideSection(
    name="Guide_2",
    w1=0.082447,
    h1=0.034941,
    w2=0.074948,
    h2=0.03916,
    l=0.9992,
    z1=2.89633,
    z2=3.89553,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    # comment="/* 2896.33 -> 3895.53 mm */",
)
guide_3 = GuideSection(
    name="Guide_3",
    w1=0.074939,
    h1=0.039164,
    w2=0.063838,
    h2=0.044511,
    l=1.47920,
    z1=3.89673,
    z2=5.37593,
    mleft=1.5,
    mright=1.5,
    mtop=4,
    mbottom=4,
    # comment="/* 3896.73 -> 5375.93 mm */",
)

guide_4a = GuideSection(
    name="Guide_4a",
    w1=0.063838,
    h1=0.04459,
    w2=0.06026,
    h2=0.04615,
    l=0.481,
    z1=5.40065,
    z2=5.88165,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    # comment="/* 5400.65 -> 5881.65 mm */",
)

guide_4b = GuideSection(
    name="Guide_4b",
    w1=0.063466,
    h1=0.044759,
    w2=0.060256,
    h2=0.046152,
    l=0.431,
    z1=5.45065,
    z2=5.88165,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    # comment="/* 5450.65 -> 5881.65 mm */",
)
guide_5 = GuideSection(
    name="Guide_5",
    w1=0.06,
    h1=0.04626,
    w2=0.06,
    h2=0.05398,
    l=2.7625,
    z1=5.916,
    z2=8.6785,
    mleft=1.5,
    mright=1.5,
    mtop=3.5,
    mbottom=3.5,
    # comment="/* 5916.00 -> 8678.50 mm */",
)
