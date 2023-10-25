from __future__ import annotations

import typing as t
from contextlib import ContextDecorator
from multiprocessing import Process
from pathlib import Path

from pxblat.extc import ServerOption, UsageStats, pystartServer

from .basic import (
    check_port_in_use,
    files,
    find_free_port,
    server_query,
    status_server,
    stop_server,
    wait_server_ready,
)

if t.TYPE_CHECKING:
    from .status import Status


def _pystartServer(
    hostName: str,
    portName: str,
    seqFiles: list[str],
    options: ServerOption,
    stats: UsageStats,
):
    pystartServer(hostName, portName, len(seqFiles), seqFiles, options, stats)


def create_server_option() -> ServerOption:
    """Creates a new ServerOption object with default values.

    Returns:
        ServerOption: A new ServerOption object with default values.

    See Also:
        :class:`.ServerOption`
    """
    return ServerOption()


class Server(ContextDecorator):
    """A context manager and decorator for managing a server process.

    This class can be used as a context manager or decorator to manage a server process. It starts the server with the given
    options, and can run it as a daemon process or block until it is ready.

    Attributes:
        host (str): The hostname or IP address to bind the server to.
        port (int): The port number to bind the server to.
        two_bit (Path | str): The path to the 2bit file or the URL of the 2bit file.
        option (ServerOption): The options to use when starting the server.
        daemon (bool, optional): Whether to run the server as a daemon process. Defaults to True.
        use_others (bool, optional): Whether to allow other users to access the server. Defaults to False.
        timeout (int, optional): The number of seconds to wait for the server to start. Defaults to 60.
        block (bool, optional): Whether to block until the server is ready. Defaults to False.

    Raises:
        ValueError: If the given two_bit file or URL is invalid.
        OSError: If there is an error starting the server process.

    Order:
        -10
    """

    def __init__(
        self,
        host: str,
        port: int,
        two_bit: Path | str,
        *,
        can_stop: bool = True,
        mask: bool = False,
        tile_size: int = 11,
        step_size: int = 11,
        max_aa_size: int = 8000,
        max_dna_hits: int = 100,
        max_gap: int = 2,
        max_nt_size: int = 40000,
        max_trans_hits: int = 200,
        min_match: int = 2,
        rep_match: int = 0,
        seq_log: bool = False,
        ip_log: bool = False,
        debug_log: bool = False,
        trans: bool = False,
        syslog: bool = False,
        no_simp_rep_mask: bool = False,
        log: str | Path | None = None,
        log_facility: str | None = None,
        per_seq_max: str | Path | None = None,
        index_file: str | Path | None = None,
        daemon=True,
        use_others: bool = False,
        timeout: int = 60,
        block: bool = False,
    ) -> None:
        """Initializes a gfServer object with the given parameters.

        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
            two_bit (Path | str): The path to the 2bit file or the URL of the 2bit file.
            can_stop (bool, optional): Whether to allow the server to be stopped. Defaults to True.
            mask (bool, optional): Whether to use masking from the 2bit file. Defaults to False.
            tile_size (int, optional): The size of n-mers to index. Defaults to 11 for nucleotides, 4 for proteins (or translated nucleotides).
            step_size (int, optional): The spacing between tiles. Defaults to tileSize.
            max_aa_size (int, optional): The maximum size of protein or translated DNA queries. Defaults to 8000.
            max_dna_hits (int, optional): The maximum number of hits for a DNA query that are sent from the server. Defaults to 100.
            max_gap (int, optional): The number of insertions or deletions allowed between n-mers. Defaults to 2 for nucleotides, 0 for proteins.
            max_nt_size (int, optional): The maximum size of untranslated DNA query sequence. Defaults to 40000.
            max_trans_hits (int, optional): The maximum number of hits for a translated query that are sent from the server. Defaults to 200.
            min_match (int, optional): The number of n-mer matches that trigger detailed alignment. Defaults to 2 for nucleotides, 3 for proteins.
            rep_match (int, optional): The number of occurrences of a tile (n-mer) that triggers repeat masking the tile. Defaults to 0.
            seq_log (bool, optional): Whether to include sequences in the log file (not logged with syslog). Defaults to False.
            ip_log (bool, optional): Whether to include user's IP in the log file (not logged with syslog). Defaults to False.
            debug_log (bool, optional): Whether to include debugging info in the log file. Defaults to False.
            trans (bool, optional): Whether to translate database to protein in 6 frames, and it is best to run this on RepeatMasked data. Defaults to False.
            syslog (bool, optional): Whether to log to syslog. Defaults to False.
            no_simp_rep_mask (bool, optional): Whether to suppress simple repeat masking. Defaults to False.
            log (str | Path | None, optional): The path to the log file that records server requests. Defaults to None.
            log_facility (str | None, optional): The syslog facility to log to. Defaults to None.
            per_seq_max (str | Path | None, optional): The path to a file that contains one seq filename (possibly with ':seq' suffix) per line. Defaults to None.
            index_file (str | Path | None, optional): The path to the index file created by `gfServer index`.
                Saving index can speed up `gfServer` startup by two orders of magnitude. Defaults to None.
            daemon (bool, optional): Whether to run the server as a daemon process. Defaults to True.
            use_others (bool, optional): Whether to allow other users to access the server. Defaults to False.
            timeout (int, optional): The number of seconds to wait for the server to start. Defaults to 60.
            block (bool, optional): Whether to block until the server is ready. Defaults to False.

        Raises:
            ValueError: If the given two_bit file or URL is invalid.
            OSError: If there is an error starting the server process.

        Returns:
            None

        Examples:
            Create a server object with options.

            >>> from pxblat import Server
            >>> server = Server("localhost", 65000, "tests/data/test_ref.2bit", can_stop=True, step_size=5)
            >>> server.start()
            >>> server.wait_ready()
            >>> server.stop()
            >>> server.can_stop
            True
            >>> server.step_size = 10
            >>> server.step_size
            10
        """
        self._host = host
        self._port = port

        self.two_bit = two_bit

        log = "" if log is None else str(log)
        log_facility = "" if log_facility is None else str(log_facility)
        per_seq_max = "" if per_seq_max is None else str(per_seq_max)
        index_file = "" if index_file is None else str(index_file)

        self.option = (
            create_server_option()
            .withCanStop(can_stop)
            .withLog(log)
            .withLogFacility(log_facility)
            .withMask(mask)
            .withMaxAaSize(max_aa_size)
            .withMaxDnaHits(max_dna_hits)
            .withMaxGap(max_gap)
            .withMaxNtSize(max_nt_size)
            .withMaxTransHits(max_trans_hits)
            .withMinMatch(min_match)
            .withRepMatch(rep_match)
            .withSeqLog(seq_log)
            .withIpLog(ip_log)
            .withDebugLog(debug_log)
            .withTileSize(tile_size)
            .withStepSize(step_size)
            .withTrans(trans)
            .withSyslog(syslog)
            .withPerSeqMax(per_seq_max)
            .withNoSimpRepMask(no_simp_rep_mask)
            .withIndexFile(index_file)
        )

        self.stat = UsageStats()

        self.use_others = use_others
        self.timeout = timeout
        self.daemon = daemon

        self._block = block
        self._is_ready = False
        self._is_open = True
        self._process = None

    @property
    def host(self):
        """The hostname or IP address to bind the server to."""
        return self._host

    @host.setter
    def host(self, value: str):
        """Sets the hostname or IP address to bind the server to."""
        self._host = value

    @property
    def port(self) -> int:
        """The port number to bind the server to."""
        return self._port

    @port.setter
    def port(self, value: int):
        """Sets the port number to bind the server to."""
        self._port = value

    def _start_b(self):
        """Start server in blocking mode."""
        two_bit_file = self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        try:
            if check_port_in_use(self.host, self.port):
                if self.use_others:
                    self._is_open = False
                    # WARN: Use server that is already open. However, the server may be not opened by gfServer <05-16-23>
                    # Hence, the `wait_server_ready` may be timeout.

                else:
                    self._is_open = True
                    new_port = find_free_port(self.host, start=self.port + 1)
                    self.port = new_port
                    pystartServer(
                        self.host,
                        str(self.port),
                        1,
                        [two_bit_file],
                        self.option,
                        self.stat,
                    )
            else:
                pystartServer(
                    self.host,
                    str(self.port),
                    1,
                    [two_bit_file],
                    self.option,
                    self.stat,
                )
        except Exception as e:
            raise e

    def _start_nb(self):
        two_bit_file = self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        try:
            if check_port_in_use(self.host, self.port):
                if self.use_others:
                    self._is_open = False
                else:
                    self._is_open = True
                    new_port = find_free_port(self._host, start=self.port + 1)
                    self.port = new_port
                    host = self.host
                    port = self.port

                    self._process = Process(
                        target=_pystartServer,
                        args=(
                            host,
                            str(port),
                            [two_bit_file],
                            self.option,
                            self.stat,
                        ),
                        daemon=self.daemon,
                    )

            else:
                self._is_open = True
                self._process = Process(
                    target=_pystartServer,
                    args=(
                        self.host,
                        str(self.port),
                        [two_bit_file],
                        self.option,
                        self.stat,
                    ),
                    daemon=self.daemon,
                )
        except Exception as e:
            raise e

        else:
            if self._process is not None:
                self._process.start()

    def _check(self):
        if not Path(self.two_bit).exists():
            msg = f"Invalid two_bit file: {self.two_bit}"
            raise FileNotFoundError(msg)

    def start(self):
        """Starts the gfServer instance in either blocking or non-blocking mode.

        If the server is set to non-blocking mode, it will start the server in a separate process.
        If the server is set to blocking mode, it will start the server in the current process.

        Raises:
            ValueError: If the given two_bit file or URL is invalid.
        """
        self.option.build()
        if not self._block:
            self._start_nb()
        else:
            self._start_b()

    def stop(self):
        """Stops the gfServer instance if it is running.

        This method sends a stop signal to the server process, causing it to terminate gracefully.

        See Also:
            :func:`stop_server` is a free function to stop a server.
        """
        if self._is_open:
            stop_server(self.host, self.port)

        if self._process is not None:
            self._process.terminate()

        self._is_open = False
        self._is_ready = False

    def status(self, *, instance=False) -> dict[str, str] | Status:
        """Retrieves the status of the gfServer instance.

        Args:
            instance (bool, optional): If True, returns a Status object. If False, returns a dictionary with status information. Defaults to False.

        Returns:
            t.Union[t.Dict[str, str], Status]: The status of the gfServer instance, either as a dictionary or a Status object.

        See Also:
            :func:`status_server` is a free function to query server status.
        """
        return status_server(self.host, self.port, self.option, instance=instance)

    def files(self) -> list[str]:
        """Retrieves the list of files served by the gfServer instance.

        Returns:
            list[str]: A list of file names served by the gfServer instance.

        See Also:
            :func:`files` is a free function to query file status for server.
        """
        return files(self.host, self.port)

    def query(self, intype: str, faName: str, *, isComplex: bool, isProt: bool) -> str:
        """Queries the gfServer instance with the given parameters.

        Args:
            intype (str): The type of input sequence. Must be one of "dna", "rna", or "protein".
            faName (str): The name of the input sequence.
            isComplex (bool): Whether the input sequence is complex.
            isProt (bool): Whether the input sequence is a protein sequence.

        Returns:
            str: The result of the query as a string.
        """
        return server_query(
            intype,
            self.host,
            self.port,
            faName,
            isComplex=isComplex,
            isProt=isProt,
        )

    def is_ready(self) -> bool:
        """Returns True if the server is ready to accept queries, False otherwise.

        Returns:
            bool: True if the server is ready to accept queries, False otherwise.
        """
        return self._is_ready

    def is_open(self) -> bool:
        """Returns True if the server is open, False otherwise.

        Returns:
            bool: True if the server is open, False otherwise.
        """
        return self._is_open

    def wait_ready(self, timeout: int = 60, *, restart: bool = False):
        """Wait server ready in block mode.

        Args:
            timeout: Timeout for wait server ready.
            restart: If timeout, restart server and wait again.

        Raises:
            RuntimeError: If server is not opened by gfServer or the server takes longer time to be ready, the `wait_server_ready` may be timeout.
            If `restart` is True, the server will be restarted and wait again.
        """
        if not self._is_ready:
            try:
                wait_server_ready(self.host, self.port, timeout, self.option)
            except RuntimeError as e:
                if restart and self.use_others:
                    self.use_others = False
                    self.start()
                    self.wait_ready(timeout * 2, restart=restart)
                else:
                    msg = f"Timeout for Waiting for {self.host} {self.port} server ready due to server is not opened by gfServer or need longer time to wait"
                    raise RuntimeError(
                        msg,
                    ) from e
            else:
                self._is_ready = True

    def __str__(self) -> str:
        """Return server option as a string."""
        return f"Server({self.host}, {self.port}, ready: {self.is_ready()} open: {self.is_open()}\n{self.option})"

    __repr__ = __str__

    def __enter__(self):
        """Starts the gfServer instance in blocking mode when used as a context manager."""
        self.start()
        return self

    def __exit__(self, *exc):
        """Stops the gfServer."""
        self.stop()

    # fmt: off
    @property
    def can_stop(self) -> bool: return self.option.canStop
    @can_stop.setter
    def can_stop(self, value: bool): self.option.canStop = value
    @property
    def log(self) -> str: return self.option.log
    @log.setter
    def log(self, value: str): self.option.log = value
    @property
    def log_facility(self) -> str: return self.option.logFacility
    @log_facility.setter
    def log_facility(self, value: str): self.option.logFacility = value
    @property
    def mask(self) -> bool: return self.option.mask
    @mask.setter
    def mask(self, value: bool): self.option.mask = value
    @property
    def max_aa_size(self) -> int: return self.option.maxAaSize
    @max_aa_size.setter
    def max_aa_size(self, value: int): self.option.maxAaSize = value
    @property
    def max_dna_hits(self) -> int: return self.option.maxDnaHits
    @max_dna_hits.setter
    def max_dna_hits(self, value: int): self.option.maxDnaHits = value
    @property
    def max_gap(self) -> int: return self.option.maxGap
    @max_gap.setter
    def max_gap(self, value: int): self.option.maxGap = value
    @property
    def max_nt_size(self) -> int: return self.option.maxNtSize
    @max_nt_size.setter
    def max_nt_size(self, value: int): self.option.maxNtSize = value
    @property
    def max_trans_hits(self) -> int: return self.option.maxTransHits
    @max_trans_hits.setter
    def max_trans_hits(self, value: int): self.option.maxTransHits = value
    @property
    def min_match(self) -> int: return self.option.minMatch
    @min_match.setter
    def min_match(self, value: int): self.option.minMatch = value
    @property
    def rep_match(self) -> int: return self.option.repMatch
    @rep_match.setter
    def rep_match(self, value: int): self.option.repMatch = value
    @property
    def seq_log(self) -> bool: return self.option.seqLog
    @seq_log.setter
    def seq_log(self, value: bool): self.option.seqLog = value
    @property
    def ip_log(self) -> bool: return self.option.ipLog
    @ip_log.setter
    def ip_log(self, value: bool): self.option.ipLog = value
    @property
    def debug_log(self) -> bool: return self.option.debugLog
    @debug_log.setter
    def debug_log(self, value: bool): self.option.debugLog = value
    @property
    def trans(self) -> bool: return self.option.trans
    @trans.setter
    def trans(self, value: bool): self.option.trans = value
    @property
    def syslog(self) -> bool: return self.option.syslog
    @syslog.setter
    def syslog(self, value: bool): self.option.syslog= value
    @property
    def no_simp_rep_mask(self) -> bool: return self.option.noSimpRepMask
    @no_simp_rep_mask.setter
    def no_simp_rep_mask(self, value: bool): self.option.noSimpRepMask= value
    @property
    def per_seq_max(self) -> str: return self.option.perSeqMax
    @per_seq_max.setter
    def per_seq_max(self, value: str): self.option.perSeqMax = value
    @property
    def index_file(self) -> str: return self.option.indexFile
    @index_file.setter
    def index_file(self, value: str): self.option.indexFile= value
    # fmt: on
