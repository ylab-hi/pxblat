from dataclasses import dataclass, field

from mashumaro import (
    DataClassDictMixin,  # type: ignore
    field_options,  # type: ignore
)
from mashumaro.mixins.json import DataClassJSONMixin  # type: ignore


@dataclass
class Status(DataClassJSONMixin, DataClassDictMixin):
    """A data class representing the status of a server.

    Attributes:
        version (str): The version of the server.
        serverType (str): The type of the server.
        types (str): The type of the server, an alias for 'serverType'.
        host (str): The hostname or IP address of the server.
        port (int): The port number the server is listening on.
        tileSize (int): The tile size used by the server.
        stepSize (int): The step size used by the server.
        minMatch (int): The minimum match used by the server.
        pcr_requests (int): The number of PCR requests the server has handled, an alias for 'pcr requests'.
        blat_requests (int): The number of BLAT requests the server has handled, an alias for 'blat requests'.
        bases (int): The number of bases processed by the server.
        misses (int): The number of misses by the server.
        noSig (int): The number of 'noSig' (no signature) events by the server.
        trimmed (int): The number of trimmed events by the server.
        warnings (int): The number of warnings issued by the server.
    """

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
