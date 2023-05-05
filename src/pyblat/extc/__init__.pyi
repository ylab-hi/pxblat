"""pybind11 plugin"""
from __future__ import annotations
import typing

__all__ = [
    "buildIndex",
    "faToTwoBit",
    "genoFindDirect",
    "genoPcrDirect",
    "getFileList",
    "gfServerOption",
    "pcrServer",
    "queryServer",
    "startServer",
    "statusServer",
    "stopServer",
]

class gfServerOption:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: gfServerOption) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> gfServerOption: ...
    def withCanStop(self, withCanStop: bool) -> gfServerOption: ...
    def withDebugLog(self, withDebugLog: bool) -> gfServerOption: ...
    def withIndexFile(self, withIndexFile: str) -> gfServerOption: ...
    def withIpLog(self, withIpLog: bool) -> gfServerOption: ...
    def withLog(self, withLog: str) -> gfServerOption: ...
    def withLogFacility(self, withLogFacility: str) -> gfServerOption: ...
    def withMask(self, withMask: bool) -> gfServerOption: ...
    def withMaxAaSize(self, withMaxAaSize: int) -> gfServerOption: ...
    def withMaxDnaHits(self, withMaxDnaHits: int) -> gfServerOption: ...
    def withMaxGap(self, withMaxGap: int) -> gfServerOption: ...
    def withMaxNtSize(self, withMaxNtSize: int) -> gfServerOption: ...
    def withMaxTransHits(self, withMaxTransHits: int) -> gfServerOption: ...
    def withMinMatch(self, withMinMatch: int) -> gfServerOption: ...
    def withNoSimpRepMask(self, withNoSimpRepMask: bool) -> gfServerOption: ...
    def withPerSeqMax(self, withPerSeqMax: str) -> gfServerOption: ...
    def withRepMatch(self, withRepMatch: int) -> gfServerOption: ...
    def withSeqLog(self, withSeqLog: bool) -> gfServerOption: ...
    def withStepSize(self, withStepSize: int) -> gfServerOption: ...
    def withSyslog(self, withSyslog: bool) -> gfServerOption: ...
    def withTileSize(self, withTileSize: int) -> gfServerOption: ...
    def withTimeout(self, withTimeout: int) -> gfServerOption: ...
    def withTrans(self, withTrans: bool) -> gfServerOption: ...
    @property
    def allowOneMismatch(self) -> bool:
        """
        :type: bool
        """
    @allowOneMismatch.setter
    def allowOneMismatch(self, arg0: bool) -> None:
        pass
    @property
    def canStop(self) -> bool:
        """
        :type: bool
        """
    @canStop.setter
    def canStop(self, arg0: bool) -> None:
        pass
    @property
    def debugLog(self) -> bool:
        """
        :type: bool
        """
    @debugLog.setter
    def debugLog(self, arg0: bool) -> None:
        pass
    @property
    def genome(self) -> str:
        """
        :type: str
        """
    @genome.setter
    def genome(self, arg0: str) -> None:
        pass
    @property
    def genomeDataDir(self) -> str:
        """
        :type: str
        """
    @genomeDataDir.setter
    def genomeDataDir(self, arg0: str) -> None:
        pass
    @property
    def indexFile(self) -> str:
        """
        :type: str
        """
    @indexFile.setter
    def indexFile(self, arg0: str) -> None:
        pass
    @property
    def ipLog(self) -> bool:
        """
        :type: bool
        """
    @ipLog.setter
    def ipLog(self, arg0: bool) -> None:
        pass
    @property
    def log(self) -> str:
        """
        :type: str
        """
    @log.setter
    def log(self, arg0: str) -> None:
        pass
    @property
    def logFacility(self) -> str:
        """
        :type: str
        """
    @logFacility.setter
    def logFacility(self, arg0: str) -> None:
        pass
    @property
    def mask(self) -> bool:
        """
        :type: bool
        """
    @mask.setter
    def mask(self, arg0: bool) -> None:
        pass
    @property
    def maxAaSize(self) -> int:
        """
        :type: int
        """
    @maxAaSize.setter
    def maxAaSize(self, arg0: int) -> None:
        pass
    @property
    def maxDnaHits(self) -> int:
        """
        :type: int
        """
    @maxDnaHits.setter
    def maxDnaHits(self, arg0: int) -> None:
        pass
    @property
    def maxGap(self) -> int:
        """
        :type: int
        """
    @maxGap.setter
    def maxGap(self, arg0: int) -> None:
        pass
    @property
    def maxNtSize(self) -> int:
        """
        :type: int
        """
    @maxNtSize.setter
    def maxNtSize(self, arg0: int) -> None:
        pass
    @property
    def maxTransHits(self) -> int:
        """
        :type: int
        """
    @maxTransHits.setter
    def maxTransHits(self, arg0: int) -> None:
        pass
    @property
    def minMatch(self) -> int:
        """
        :type: int
        """
    @minMatch.setter
    def minMatch(self, arg0: int) -> None:
        pass
    @property
    def noSimpRepMask(self) -> bool:
        """
        :type: bool
        """
    @noSimpRepMask.setter
    def noSimpRepMask(self, arg0: bool) -> None:
        pass
    @property
    def perSeqMax(self) -> str:
        """
        :type: str
        """
    @perSeqMax.setter
    def perSeqMax(self, arg0: str) -> None:
        pass
    @property
    def repMatch(self) -> int:
        """
        :type: int
        """
    @repMatch.setter
    def repMatch(self, arg0: int) -> None:
        pass
    @property
    def seqLog(self) -> bool:
        """
        :type: bool
        """
    @seqLog.setter
    def seqLog(self, arg0: bool) -> None:
        pass
    @property
    def stepSize(self) -> int:
        """
        :type: int
        """
    @stepSize.setter
    def stepSize(self, arg0: int) -> None:
        pass
    @property
    def syslog(self) -> bool:
        """
        :type: bool
        """
    @syslog.setter
    def syslog(self, arg0: bool) -> None:
        pass
    @property
    def tileSize(self) -> int:
        """
        :type: int
        """
    @tileSize.setter
    def tileSize(self, arg0: int) -> None:
        pass
    @property
    def timeout(self) -> int:
        """
        :type: int
        """
    @timeout.setter
    def timeout(self, arg0: int) -> None:
        pass
    @property
    def trans(self) -> bool:
        """
        :type: bool
        """
    @trans.setter
    def trans(self, arg0: bool) -> None:
        pass
    pass

def buildIndex(
    gfxFile: str, fileCount: int, seqFiles: typing.List[str], options: gfServerOption
) -> None:
    pass

def faToTwoBit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
    useLong: bool = False,
) -> None:
    """
    A function that converts FASTA files to twoBit files:
     long:     use 64-bit offsets for index
    noMask: Ignore lower-case masking in fa file.
    stripVersion:  Strip off version number after .
    ignoreDups:    Convert first sequence only if there are duplicate sequence names.
    """

def genoFindDirect(
    probeName: str, fileCount: int, seqFiles: typing.List[str], options: gfServerOption
) -> None:
    """
    genoFindDirect
    """

def genoPcrDirect(
    fPrimer: str,
    rPrimer: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: gfServerOption,
) -> None:
    """
    A function that performs PCR on genomic sequences
    """

def getFileList(hostName: str, arg1: str) -> None:
    pass

def pcrServer(
    hostName: str, portName: str, fPrimer: str, rPrimer: str, maxSize: int
) -> None:
    pass

def queryServer(
    type: str, hostName: str, portName: str, faName: str, complex: bool, isProt: bool
) -> None:
    """
    queryServer
    """

def startServer(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: gfServerOption,
) -> None:
    """
    startServer
    """

def statusServer(hostName: str, portName: str, options: gfServerOption) -> int:
    pass

def stopServer(hostName: str, portName: str) -> None:
    """
    stop sever
    """
