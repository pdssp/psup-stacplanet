from enum import StrEnum, auto

from pydantic import AnyUrl, ConfigDict
from stac_pydantic.shared import StacBaseModel


class SolSysTargets(StrEnum):
    """Accepted values for the planetary body's target class
    according to the IVOA.
    """

    ASTEROID = auto()
    DWARF_PLANET = auto()
    PLANET = auto()
    SATELLITE = auto()
    COMET = auto()
    EXOPLANET = auto()
    INTERPLANETARY_MEDIUM = auto()
    SAMPLE = auto()
    SKY = auto()
    SPACECRAFT = auto()
    SPACEJUNK = auto()
    STAR = auto()
    CALIBRATION = auto()


class SolSysItemExtension(StacBaseModel):
    """https://github.com/stac-extensions/ssys"""

    targets: list[str] | None = None
    local_time: str | None = None
    target_class: SolSysTargets | None = None

    model_config = ConfigDict(extra="ignore", alias_generator=lambda s: "ssys:" + s)

    @property
    def stac_extension_url(self) -> AnyUrl:
        return AnyUrl("https://stac-extensions.github.io/ssys/v1.1.1/schema.json")


class PdsspItemExtension(StacBaseModel):
    """https://pdssp.github.io/stacplanet/v1.1.0/schema.json"""
