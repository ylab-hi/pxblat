"""Bindings for ::cppbinding namespace"""
from __future__ import annotations
import pxblat._extc.cppbinding  # type: ignore
import typing

__all__ = [
    "Signal",
    "UsageStats",
    "buildIndex",
    "faToTwoBit",
    "genoFindDirect",
    "genoPcrDirect",
    "getFileList",
    "getPortIx",
    "gfClientOption",
    "gfServer",
    "gfServerOption",
    "pcrServer",
    "pygetFileList",
    "pygfClient",
    "pyqueryServer",
    "pystartServer",
    "pystatusServer",
    "queryServer",
    "startServer",
    "statusServer",
    "stopServer",
    "test_add",
    "test_exception",
    "test_stat",
    "test_stdout",
]

class Signal:
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    @property
    def isReady(self) -> bool:
        """
        :type: bool
        """
    @isReady.setter
    def isReady(self, arg0: bool) -> None:
        pass
    pass

class UsageStats:
    def __init__(self) -> None: ...
    def __str__(self) -> str: ...
    @property
    def aaCount(self) -> int:
        """
        :type: int
        """
    @aaCount.setter
    def aaCount(self, arg0: int) -> None:
        pass
    @property
    def baseCount(self) -> int:
        """
        :type: int
        """
    @baseCount.setter
    def baseCount(self, arg0: int) -> None:
        pass
    @property
    def blatCount(self) -> int:
        """
        :type: int
        """
    @blatCount.setter
    def blatCount(self, arg0: int) -> None:
        pass
    @property
    def missCount(self) -> int:
        """
        :type: int
        """
    @missCount.setter
    def missCount(self, arg0: int) -> None:
        pass
    @property
    def noSigCount(self) -> int:
        """
        :type: int
        """
    @noSigCount.setter
    def noSigCount(self, arg0: int) -> None:
        pass
    @property
    def pcrCount(self) -> int:
        """
        :type: int
        """
    @pcrCount.setter
    def pcrCount(self, arg0: int) -> None:
        pass
    @property
    def trimCount(self) -> int:
        """
        :type: int
        """
    @trimCount.setter
    def trimCount(self, arg0: int) -> None:
        pass
    @property
    def warnCount(self) -> int:
        """
        :type: int
        """
    @warnCount.setter
    def warnCount(self, arg0: int) -> None:
        pass
    pass

class gfClientOption:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: gfClientOption) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::build() --> struct cppbinding::gfClientOption &
        """
    def to_string(self) -> str:
        """
        C++: cppbinding::gfClientOption::to_string() const --> std::string
        """
    def withDots(self, dots_: int) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withDots(int) --> struct cppbinding::gfClientOption &
        """
    def withGenome(self, genome_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withGenome(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withGenomeDataDir(self, genomeDataDir_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withGenomeDataDir(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withHost(self, hostName_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withHost(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withInName(self, inName_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withInName(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withInSeq(self, inseq_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withInSeq(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withIsDynamic(self, isDynamic_: bool) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withIsDynamic(bool) --> struct cppbinding::gfClientOption &
        """
    def withMaxIntron(self, maxIntron_: int) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withMaxIntron(long) --> struct cppbinding::gfClientOption &
        """
    def withMinIdentity(self, minIdentity_: float) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withMinIdentity(double) --> struct cppbinding::gfClientOption &
        """
    def withMinScore(self, minScore_: int) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withMinScore(int) --> struct cppbinding::gfClientOption &
        """
    def withNohead(self, nohead_: bool) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withNohead(bool) --> struct cppbinding::gfClientOption &
        """
    def withOutName(self, outName_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withOutName(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withOutputFormat(self, outputFormat_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withOutputFormat(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withPort(self, portName_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withPort(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withQType(self, qType_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withQType(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withSeqDir(self, SeqDir_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withSeqDir(const std::string &) --> struct cppbinding::gfClientOption &
        """
    def withTType(self, tType_: str) -> gfClientOption:
        """
        C++: cppbinding::gfClientOption::withTType(const std::string &) --> struct cppbinding::gfClientOption &
        """
    @property
    def SeqDir(self) -> str:
        """
        :type: str
        """
    @SeqDir.setter
    def SeqDir(self, arg0: str) -> None:
        pass
    @property
    def dots(self) -> int:
        """
        :type: int
        """
    @dots.setter
    def dots(self, arg0: int) -> None:
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
    def hostName(self) -> str:
        """
        :type: str
        """
    @hostName.setter
    def hostName(self, arg0: str) -> None:
        pass
    @property
    def inName(self) -> str:
        """
        :type: str
        """
    @inName.setter
    def inName(self, arg0: str) -> None:
        pass
    @property
    def inSeq(self) -> str:
        """
        :type: str
        """
    @inSeq.setter
    def inSeq(self, arg0: str) -> None:
        pass
    @property
    def isDynamic(self) -> bool:
        """
        :type: bool
        """
    @isDynamic.setter
    def isDynamic(self, arg0: bool) -> None:
        pass
    @property
    def maxIntron(self) -> int:
        """
        :type: int
        """
    @maxIntron.setter
    def maxIntron(self, arg0: int) -> None:
        pass
    @property
    def minIdentity(self) -> float:
        """
        :type: float
        """
    @minIdentity.setter
    def minIdentity(self, arg0: float) -> None:
        pass
    @property
    def minScore(self) -> int:
        """
        :type: int
        """
    @minScore.setter
    def minScore(self, arg0: int) -> None:
        pass
    @property
    def nohead(self) -> bool:
        """
        :type: bool
        """
    @nohead.setter
    def nohead(self, arg0: bool) -> None:
        pass
    @property
    def outName(self) -> str:
        """
        :type: str
        """
    @outName.setter
    def outName(self, arg0: str) -> None:
        pass
    @property
    def outputFormat(self) -> str:
        """
        :type: str
        """
    @outputFormat.setter
    def outputFormat(self, arg0: str) -> None:
        pass
    @property
    def portName(self) -> str:
        """
        :type: str
        """
    @portName.setter
    def portName(self, arg0: str) -> None:
        pass
    @property
    def qType(self) -> str:
        """
        :type: str
        """
    @qType.setter
    def qType(self, arg0: str) -> None:
        pass
    @property
    def tType(self) -> str:
        """
        :type: str
        """
    @tType.setter
    def tType(self, arg0: str) -> None:
        pass
    pass

class gfServerOption:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: gfServerOption) -> None: ...
    def __str__(self) -> str: ...
    def build(self) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::build() --> struct cppbinding::gfServerOption &
        """
    def to_string(self) -> str:
        """
        C++: cppbinding::gfServerOption::to_string() const --> std::string
        """
    def withCanStop(self, canStop_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withCanStop(bool) --> struct cppbinding::gfServerOption &
        """
    def withDebugLog(self, debugLog_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withDebugLog(bool) --> struct cppbinding::gfServerOption &
        """
    def withIndexFile(self, indexFile_: str) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withIndexFile(std::string) --> struct cppbinding::gfServerOption &
        """
    def withIpLog(self, ipLog_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withIpLog(bool) --> struct cppbinding::gfServerOption &
        """
    def withLog(self, log_: str) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withLog(std::string) --> struct cppbinding::gfServerOption &
        """
    def withLogFacility(self, logFacility_: str) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withLogFacility(std::string) --> struct cppbinding::gfServerOption &
        """
    def withMask(self, mask_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMask(bool) --> struct cppbinding::gfServerOption &
        """
    def withMaxAaSize(self, maxAaSize_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMaxAaSize(int) --> struct cppbinding::gfServerOption &
        """
    def withMaxDnaHits(self, maxDnaHits_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMaxDnaHits(int) --> struct cppbinding::gfServerOption &
        """
    def withMaxGap(self, maxGap_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMaxGap(int) --> struct cppbinding::gfServerOption &
        """
    def withMaxNtSize(self, maxNtSize_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMaxNtSize(int) --> struct cppbinding::gfServerOption &
        """
    def withMaxTransHits(self, maxTransHits_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMaxTransHits(int) --> struct cppbinding::gfServerOption &
        """
    def withMinMatch(self, minMatch_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withMinMatch(int) --> struct cppbinding::gfServerOption &
        """
    def withNoSimpRepMask(self, noSimpRepMask_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withNoSimpRepMask(bool) --> struct cppbinding::gfServerOption &
        """
    def withPerSeqMax(self, perSeqMax_: str) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withPerSeqMax(std::string) --> struct cppbinding::gfServerOption &
        """
    def withRepMatch(self, repMatch_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withRepMatch(int) --> struct cppbinding::gfServerOption &
        """
    def withSeqLog(self, seqLog_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withSeqLog(bool) --> struct cppbinding::gfServerOption &
        """
    def withStepSize(self, stepSize_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withStepSize(int) --> struct cppbinding::gfServerOption &
        """
    def withSyslog(self, syslog_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withSyslog(bool) --> struct cppbinding::gfServerOption &
        """
    def withThreads(self, threads_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withThreads(int) --> struct cppbinding::gfServerOption &
        """
    def withTileSize(self, tileSize_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withTileSize(int) --> struct cppbinding::gfServerOption &
        """
    def withTimeout(self, timeout_: int) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withTimeout(int) --> struct cppbinding::gfServerOption &
        """
    def withTrans(self, trans_: bool) -> gfServerOption:
        """
        C++: cppbinding::gfServerOption::withTrans(bool) --> struct cppbinding::gfServerOption &
        """
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
    def threads(self) -> int:
        """
        :type: int
        """
    @threads.setter
    def threads(self, arg0: int) -> None:
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
    """
    C++: cppbinding::buildIndex(std::string &, int, class std::vector<std::string >, const struct cppbinding::gfServerOption &) --> void
    """

@typing.overload
def faToTwoBit(inFiles: typing.List[str], outFile: str) -> int:
    """
    C++: cppbinding::faToTwoBit(class std::vector<std::string > &, std::string &, bool, bool, bool, bool) --> int
    """

@typing.overload
def faToTwoBit(inFiles: typing.List[str], outFile: str, noMask: bool) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str], outFile: str, noMask: bool, stripVersion: bool
) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool,
    stripVersion: bool,
    ignoreDups: bool,
) -> int:
    pass

@typing.overload
def faToTwoBit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool,
    stripVersion: bool,
    ignoreDups: bool,
    useLong: bool,
) -> int:
    pass

def genoFindDirect(
    probeName: str, fileCount: int, seqFiles: typing.List[str], options: gfServerOption
) -> None:
    """
    C++: cppbinding::genoFindDirect(std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) --> void
    """

def genoPcrDirect(
    fPrimer: str,
    rPrimer: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: gfServerOption,
) -> None:
    """
    C++: cppbinding::genoPcrDirect(std::string &, std::string &, int, class std::vector<std::string > &, const struct cppbinding::gfServerOption &) --> void
    """

def getFileList(hostName: str, portName: str) -> None:
    """
    C++: cppbinding::getFileList(std::string &, std::string &) --> void
    """

def getPortIx(portName: str) -> int:
    """
    C++: cppbinding::getPortIx(char *) --> int
    """

def gfServer(options: gfServerOption) -> None:
    """
    C++: cppbinding::gfServer(struct cppbinding::gfServerOption &) --> void
    """

def pcrServer(
    hostName: str, portName: str, fPrimer: str, rPrimer: str, maxSize: int
) -> None:
    """
    C++: cppbinding::pcrServer(std::string &, std::string &, std::string &, std::string &, int) --> void
    """

def pygetFileList(hostName: str, portName: str) -> str:
    """
    C++: cppbinding::pygetFileList(std::string &, std::string &) --> std::string
    """

def pygfClient(option: gfClientOption) -> str:
    """
    C++: cppbinding::pygfClient(struct cppbinding::gfClientOption &) --> std::string
    """

def pyqueryServer(
    type: str, hostName: str, portName: str, faName: str, complex: bool, isProt: bool
) -> str:
    """
    C++: cppbinding::pyqueryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) --> std::string
    """

def pystartServer(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: gfServerOption,
    stats: UsageStats,
) -> int:
    """
    C++: cppbinding::pystartServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) --> int
    """

def pystatusServer(hostName: str, portName: str, options: gfServerOption) -> str:
    """
    C++: cppbinding::pystatusServer(std::string &, std::string &, struct cppbinding::gfServerOption &) --> std::string
    """

def queryServer(
    type: str, hostName: str, portName: str, faName: str, complex: bool, isProt: bool
) -> None:
    """
    C++: cppbinding::queryServer(std::string &, std::string &, std::string &, std::string &, bool, bool) --> void
    """

def startServer(
    hostName: str,
    portName: str,
    fileCount: int,
    seqFiles: typing.List[str],
    options: gfServerOption,
    stats: UsageStats,
) -> None:
    """
    C++: cppbinding::startServer(std::string &, std::string &, int, class std::vector<std::string > &, struct cppbinding::gfServerOption &, struct cppbinding::UsageStats &) --> void
    """

def statusServer(hostName: str, portName: str, options: gfServerOption) -> int:
    """
    C++: cppbinding::statusServer(std::string &, std::string &, struct cppbinding::gfServerOption &) --> int
    """

def stopServer(hostName: str, portName: str) -> None:
    """
    C++: cppbinding::stopServer(std::string &, std::string &) --> void
    """

def test_add(a: int) -> None:
    """
    C++: cppbinding::test_add(int &) --> void
    """

def test_exception() -> None:
    """
    C++: cppbinding::test_exception() --> void
    """

def test_stat(stats: UsageStats) -> None:
    """
    C++: cppbinding::test_stat(struct cppbinding::UsageStats &) --> void
    """

def test_stdout() -> None:
    """
    C++: cppbinding::test_stdout() --> void
    """
