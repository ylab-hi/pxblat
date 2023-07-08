import tempfile
from pathlib import Path
from threading import Thread
from typing import Optional
from typing import TypeVar

from pxblat.extc import ClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read

from .basic import wait_server_ready
from .server import ServerOption

INSEQ = TypeVar("INSEQ", str, Path)


def create_client_option():
    """Creates a new ClientOption object with default values.

    Return:
        ClientOption object
    """
    return ClientOption()


def _resolve_host_port(
    client_option: ClientOption, host: Optional[str], port: Optional[int]
):
    """Resolves the host and port for the client option.

    Args:
        client_option: ClientOption object
        host: Optional[str]
        port: Optional[int]
    """
    if host is not None:
        client_option.hostName = host

    if port is not None:
        client_option.portName = str(port)

    if not client_option.hostName and not client_option.portName:
        raise ValueError("host and port are both empty")


def query_server(
    option: ClientOption,
    host: Optional[str] = None,
    port: Optional[int] = None,
    seqname: Optional[str] = None,
    parse: bool = True,
):
    """Sends a query to the server and returns the result.

    Args:
        option: ClientOption object
        host: Optional[str]
        port: Optional[int]
        seqname: Optional[str]
        parse: bool

    Returns:
        str or bytes: The result of the query.

    """
    _resolve_host_port(option, host, port)

    fafile = None
    if not option.inName and not option.inSeq:
        raise ValueError("inName and inSeq are both empty")

    if option.inSeq:
        fafile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        seqname = fafile.name if seqname is None else seqname
        fafile.write(f">{seqname}\n")
        fafile.write(option.inSeq)
        fafile.close()

        option.inName = fafile.name

    # return bytes
    ret = pygfClient(option)

    try:
        ret_decode = ret.decode().rsplit(",\n", 1)[0]  # type: ignore
    except UnicodeDecodeError:
        ret_decode = ret.decode("latin-1").rsplit(",\n", 1)[0]  # type: ignore

    if fafile is not None:
        Path(fafile.name).unlink()

    if parse and ret_decode:
        return read(ret_decode, "psl")

    return ret_decode


class Client(Thread):
    """A class for managing client connections to a server in a separate thread.

    This class can be used to query a gfServer in a separate thread, and can optionally wait until the server is ready before
    sending a query. It can also parse the result of the query.

    Attributes:
        option (ClientOption): Client options for the connection.
        host (str, optional): The hostname or IP address of the server. Defaults to None.
        port (int, optional): The port number of the server. Defaults to None.
        wait_ready (bool, optional): Whether to wait until the server is ready before sending a query. Defaults to False.
        wait_timeout (int, optional): The number of seconds to wait for the server to be ready. Defaults to 60.
        server_option (ServerOption, optional): The server options to use if a server is not provided. Defaults to None.
        seqname (str, optional): The sequence name to use for the query. Defaults to None.
        parse (bool, optional): Whether to parse the result of the query. Defaults to True.
        daemon (bool, optional): Whether to run the client as a daemon process. Defaults to True.
        result: The result of the query, or None if the query has not yet been sent or the result has not yet been received.

    Order:
        -10
    """

    def __init__(
        self,
        option: ClientOption,
        host: Optional[str] = None,
        port: Optional[int] = None,
        wait_ready: bool = False,
        wait_timeout: int = 60,
        server_option: Optional[ServerOption] = None,
        seqname: Optional[str] = None,
        parse: bool = True,
        daemon: bool = True,
    ) -> None:
        """A class for querying a gfServer using a separate thread.

        Args:
            option: ClientOption object
            host: Optional[str]
            port: Optional[int]
            wait_ready: bool
            wait_timeout: int
            server_option: Optional[ServerOption]
            seqname: Optional[str]
            parse: bool
            daemon: bool

        Attributes:
            result: The result of the query.

        """
        super().__init__(daemon=daemon)
        self.option = option
        self._host = host
        self._port = port
        self._resolve_host_port()

        self._wait_ready = wait_ready
        self._wait_timeout = wait_timeout
        self._server_option = server_option
        self._seqname = seqname
        self._parse = parse

        self.result = None

    def run(self):
        """Runs the query in a separate thread."""
        if self._wait_ready:
            wait_server_ready(
                self.host,
                self.port,
                timeout=self._wait_timeout,
                gfserver_option=self._server_option,
            )

        ret = query_server(self.option, seqname=self._seqname, parse=self._parse)

        self.result = ret

    def get(self):
        """Sends a query to the server and returns the result."""
        self.join()
        return self.result

    @property
    def host(self):
        """The hostname or IP address of the server."""
        if self._host is None:
            return self.option.hostName

        return self._host

    @host.setter
    def host(self, value: str):
        """Sets the hostname or IP address of the server."""
        self._host = value

    @property
    def port(self):
        """The port number of the server."""
        if self._port is None:
            return int(self.option.portName)

        return self._port

    @port.setter
    def port(self, value: int):
        """Sets the port number of the server."""
        self._port = value

    @classmethod
    def create_option(cls):
        """Creates a new ClientOption object with default values.

        Return:
            ClientOption object

        """
        return create_client_option()

    def _resolve_host_port(self):
        _resolve_host_port(self.option, self._host, self._port)


class Gclient:
    """A class for managing client connections to a server in a separate thread.

    This class can be used to query a gfServer in a separate thread, and can optionally wait until the server is ready before
    sending a query. It can also parse the result of the query.

    Attributes:
        option (ClientOption): Client options for the connection.
        host (str, optional): The hostname or IP address of the server. Defaults to None.
        port (int, optional): The port number of the server. Defaults to None.
        wait_ready (bool, optional): Whether to wait until the server is ready before sending a query. Defaults to False.
        wait_timeout (int, optional): The number of seconds to wait for the server to be ready. Defaults to 60.
        server_option (ServerOption, optional): The server options to use if a server is not provided. Defaults to None.
        seqname (str, optional): The sequence name to use for the query. Defaults to None.
        parse (bool, optional): Whether to parse the result of the query. Defaults to True.
        daemon (bool, optional): Whether to run the client as a daemon process. Defaults to True.
        result: The result of the query, or None if the query has not yet been sent or the result has not yet been received.

    Order:
        -10
    """

    # std::string hostName{};
    # std::string portName{};
    # std::string tType{"dna"};
    # std::string qType{"dna"};
    # int dots{0};
    # bool nohead{false};
    # int minScore{30};
    # double minIdentity{90.0};
    # std::string outputFormat{"psl"};
    # long maxIntron{ffIntronMaxDefault};
    # std::string genome{};
    # std::string genomeDataDir{};
    # bool isDynamic{false};
    # std::string SeqDir{};
    # std::string inName{};
    # std::string outName{};
    # std::string inSeq{};

    def __init__(
        self,
        host: str,
        port: int,
        *,
        ttype: str = "dna",
        qtype: str = "dna",
        dots: int = 0,
        nohead: bool = False,
        min_score: int = 30,
        min_identity: float = 90.0,
        output_format: str = "psl",
        max_intron: int = 100000,
        is_dynamic: bool = False,
        genome: Optional[str] = None,
        genome_data_dir: Optional[str] = None,
        seq_dir: Optional[str] = None,
        server_option: Optional[ServerOption] = None,
        wait_ready: bool = False,
        wait_timeout: int = 60,
        parse: bool = True,
    ) -> None:
        """A class for querying a gfServer using a separate thread."""
        self._basic_option = (
            ClientOption()
            .withHost(host)
            .withPort(str(port))
            .withMinScore(min_score)
            .withMinIdentity(min_identity)
            .withTType(ttype)
            .withQType(qtype)
            .withDots(dots)
            .withNohead(nohead)
            .withMaxIntron(max_intron)
            .withOutputFormat(output_format)
            .withIsDynamic(is_dynamic)
        )

        if genome is not None:
            self._basic_option.withGenome(genome)
        if genome_data_dir is not None:
            self._basic_option.withGenomeDataDir(genome_data_dir)
        if seq_dir is not None:
            self._basic_option.withSeqDir(seq_dir)

        self._wait_ready = wait_ready
        self._wait_timeout = wait_timeout
        self._server_option = server_option
        self._parse = parse

    @property
    def host(self):
        """The hostname or IP address of the server."""
        return self._basic_option.hostName

    @host.setter
    def host(self, value: str):
        """Sets the hostname or IP address of the server."""
        self._basic_option.withHost(value)

    @property
    def port(self):
        """The port number of the server."""
        return int(self._basic_option.portName)

    @port.setter
    def port(self, value: int):
        """Sets the port number of the server."""
        self._basic_option.withPort(str(value))

    @staticmethod
    def _verify_input(in_seqs: list[INSEQ]):
        for item in in_seqs:
            if isinstance(item, Path) and not item.exists():
                raise FileNotFoundError(f"File {item} does not exist")

    def _query(self, in_seq: INSEQ):
        if isinstance(in_seq, str):
            self._basic_option.withInSeq(in_seq).build()
        else:
            self._basic_option.withInName(str(in_seq)).build()

        return query_server(self._basic_option, parse=self._parse)

    def query(self, in_seqs: list[INSEQ]):
        self._verify_input(in_seqs)

        if self._wait_ready:
            wait_server_ready(
                self.host,
                self.port,
                timeout=self._wait_timeout,
                gfserver_option=self._server_option,
            )

        from gevent.pool import Pool

        group = Pool(len(in_seqs))

        yield from group.imap(self._query, in_seqs)
