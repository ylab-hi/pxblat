from dataclasses import dataclass
from dataclasses import field

from mashumaro import DataClassDictMixin
from mashumaro import field_options
from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Status(DataClassJSONMixin, DataClassDictMixin):
    version: str
    serverType: str
    types: str = field(metadata=field_options(alias="type"))
    host: str
    port: int
    tileSize: int
    stepSize: int
    minMatch: int
    pcr_requests: int = field(metadata=field_options(alias="pcr requests"))
    blat_requests: int = field(metadata=field_options(alias="blat requests"))
    bases: int
    misses: int
    noSig: int
    trimmed: int
    warnings: int
