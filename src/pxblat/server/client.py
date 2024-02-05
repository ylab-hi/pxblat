from __future__ import annotations

import tempfile
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING, Union

from pxblat.extc import ClientOption, pygfClient
from pxblat.parser import read

from .basic import wait_server_ready

if TYPE_CHECKING:
    from .server import ServerOption

from typing import List

INSEQ = Union[str, Path]
INSEQS = Union[List[INSEQ], List[str], List[Path]]


def copy_client_option(option: ClientOption) -> ClientOption:
    """Copies the ClientOption object."""
    new_option = ClientOption()
    new_option.hostName = option.hostName
    new_option.portName = option.portName
    new_option.tType = option.tType
    new_option.qType = option.qType
    new_option.dots = option.dots
    new_option.nohead = option.nohead
    new_option.minScore = option.minScore
    new_option.minIdentity = option.minIdentity
    new_option.outputFormat = option.outputFormat
    new_option.maxIntron = option.maxIntron
    new_option.genome = option.genome
    new_option.genomeDataDir = option.genomeDataDir
    new_option.isDynamic = option.isDynamic
    new_option.SeqDir = option.SeqDir
    new_option.inName = option.inName
    new_option.outName = option.outName
    new_option.inSeq = option.inSeq
    return new_option


def create_client_option():
    """Creates a new ClientOption object with default values.

    Return:
        ClientOption object

    See Also:
        :class:`.ClientOption`

    Examples:
        >>> option = create_client_option().build()
        >>> option
        ClientOption(hostName=, portName=, tType=dna, qType=dna, dots=0, nohead=false, minScore=30, minIdentity=90,
                     outputFormat=psl, maxIntron=750000, genome=, genomeDataDir=, isDynamic=false,
                     tSeqDir=, inName=, outName=)
        >>> option = create_client_option().withPort("66666").build()
        >>> option
        ClientOption(hostName=, portName=66666, tType=dna, qType=dna, dots=0, nohead=false, minScore=30, minIdentity=90,
                     outputFormat=psl, maxIntron=750000, genome=, genomeDataDir=, isDynamic=false,
                     tSeqDir=, inName=, outName=)
    """
    return ClientOption()


def _resolve_host_port(
    client_option: ClientOption,
    host: str | None,
    port: int | None,
):
    """Resolves the host and port for the client option.

    Args:
        client_option: ClientOption
        host: Optional[str]
        port: Optional[int]
    """
    if host is not None:
        client_option.hostName = host

    if port is not None:
        client_option.portName = str(port)

    if not client_option.hostName and not client_option.portName:
        msg = "host and port are both empty"
        raise ValueError(msg)


def query_server_by_file(
    option: ClientOption,
    host: str | None = None,
    port: int | None = None,
    *,
    parse: bool = True,
):
    """Sends a query to the server and returns the result.

    Args:
        option: ClientOption
        host: Optional[str]
        port: Optional[int]
        seqname: Optional[str]
        parse: bool

    Returns:
        str or bytes: The result of the query.

    """
    _resolve_host_port(option, host, port)

    ret = pygfClient(option)

    try:
        ret_decode = ret.decode().rsplit(",\n", 1)[0]  # type: ignore
    except UnicodeDecodeError:
        ret_decode = ret.decode("latin-1").rsplit(",\n", 1)[0]  # type: ignore

    if parse and ret_decode:
        try:
            ret = read(ret_decode, "psl")
        except ValueError as e:
            if "No query results" in str(e):
                return None
        else:
            return ret

    return ret_decode


def _assign_info_to_query_result(query_result):
    query_result.version = "v.37x1"
    return query_result


def query_server(
    option: ClientOption,
    host: str | None = None,
    port: int | None = None,
    seqname: str | None = None,
    *,
    parse: bool = True,
):
    """Sends a query to the server and returns the result.

    Args:
        option: ClientOption
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
        msg = "inName and inSeq are both empty"
        raise ValueError(msg)

    if option.inSeq:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fafile:
            seqname = fafile.name if seqname is None else seqname
            fafile.write(f">{seqname}\n")
            fafile.write(option.inSeq)
        option.inName = fafile.name

    ret = pygfClient(option)

    try:
        ret_decode = ret.decode().rsplit(",\n", 1)[0]  # type: ignore
    except UnicodeDecodeError:
        ret_decode = ret.decode("latin-1").rsplit(",\n", 1)[0]  # type: ignore

    if fafile is not None:
        Path(fafile.name).unlink()

    if not parse:
        return ret_decode

    try:
        res = read(ret_decode, "psl")
    except ValueError as e:
        if "No query results" in str(e):
            return None
        raise e
    else:
        return _assign_info_to_query_result(res)


class ClientThread(Thread):
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
        host: str | None = None,
        port: int | None = None,
        *,
        wait_timeout: int = 60,
        server_option: ServerOption | None = None,
        seqname: str | None = None,
        wait_ready: bool = False,
        parse: bool = True,
        daemon: bool = True,
    ) -> None:
        """A class for querying a gfServer using a separate thread.

        Args:
            option: ClientOption
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
                server_option=self._server_option,
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


class Client:
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
        host: str,
        port: int,
        seq_dir: str | Path,
        *,
        ttype: str = "dna",
        qtype: str = "dna",
        dots: int = 0,
        nohead: bool = False,
        min_score: int = 30,
        min_identity: float = 90.0,
        output_format: str = "psl",
        max_intron: int = 750000,
        is_dynamic: bool = False,
        genome: str | None = None,
        genome_data_dir: str | None = None,
        server_option: ServerOption | None = None,
        wait_ready: bool = False,
        wait_timeout: int = 60,
        parse: bool = True,
    ) -> None:
        """A class for querying a gfServer using a separate thread.

        Args:
            host (str): The hostname or IP address of the server.
            port (int): The port number of the server.
            seq_dir (Union[str, Path]): The directory where sequence data is stored.
            ttype (str, optional): Database type. One of 'dna', 'prot', 'dnax'. Default is 'dna'.
            qtype (str, optional): Query type. One of 'dna', 'rna', 'prot', 'dnax', 'rnax'. Default is 'dna'.
            dots (int, optional): Output a dot every N query sequences. Default is 0.
            nohead (bool, optional): If True, suppresses 5-line psl header. Default is False.
            min_score (int, optional): Sets minimum score. Default is 30.
            min_identity (float, optional): Sets minimum sequence identity (in percent). Default is 90.
            output_format (str, optional): Controls output file format. One of 'psl', 'pslx', 'axt', 'maf', 'sim4', 'wublast', 'blast', 'blast8', 'blast9'. Default is 'psl'.
            max_intron (int, optional): Sets maximum intron size. Default is 750000.
            is_dynamic (bool, optional): If True, the client is expected to interact with a dynamic gfServer. Default is False.
            genome (Optional[str], optional): The genome name when using a dynamic gfServer. Defaults to None.
            genome_data_dir (Optional[str], optional): The root directory containing the genome data files for a dynamic gfServer. Defaults to None.
            server_option (Optional[ServerOption], optional): The server options to use if a server is not provided. Defaults to None.
            wait_ready (bool, optional): If True, wait until the server is ready before sending a query. Default is False.
            wait_timeout (int, optional): The number of seconds to wait for the server to be ready. Default is 60.
            parse (bool, optional): If True, parse the result of the query. Default is True.

        Raises:
            ValueError: If any of the input values are invalid.

        Examples:
            >>> from pxblat import Client
            >>> host = "localhost"
            >>> port = 65000
            >>> seq_dir = "."
            >>> two_bit = "./test_ref.2bit"
            >>> client = Client(
            ...     host=host,
            ...     port=port,
            ...     seq_dir=seq_dir,
            ...     min_score=20,
            ...     min_identity=90,
            ... )
        """
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

        self._basic_option.withSeqDir(str(seq_dir))

        self._wait_ready = wait_ready
        self._wait_timeout = wait_timeout
        self._server_option = server_option
        self._parse = parse

    # fmt: off
    @property
    def seq_dir(self):
        """The directory containing the sequence files."""
        return self._basic_option.SeqDir
    @seq_dir.setter
    def seq_dir(self, value: str | Path): self._basic_option.withSeqDir(str(value))

    @property
    def ttype(self):
        """The type of the target sequence."""
        return self._basic_option.tType
    @ttype.setter
    def ttype(self, value: str): self._basic_option.withTType(value)

    @property
    def qtype(self):
        """The type of the query sequence."""
        return self._basic_option.qType
    @qtype.setter
    def qtype(self, value: str): self._basic_option.withQType(value)

    @property
    def min_score(self):
        """The minimum score for the alignment."""
        return int(self._basic_option.minScore)
    @min_score.setter
    def min_score(self, value: int): self._basic_option.withMinScore(value)

    @property
    def min_identity(self):
        """The minimum identity for the alignment."""
        return self._basic_option.minIdentity
    @min_identity.setter
    def min_identity(self, value: float): self._basic_option.withMinIdentity(value)

    @property
    def host(self):
        """The hostname or IP address of the server."""
        return self._basic_option.hostName
    @host.setter
    def host(self, value: str): self._basic_option.withHost(value)

    @property
    def port(self):
        """The port number of the server."""
        return int(self._basic_option.portName)
    @port.setter
    def port(self, value: int): self._basic_option.withPort(str(value))

    @property
    def output_format(self):
        """The output format of the alignment."""
        return self._basic_option.outputFormat
    @output_format.setter
    def output_format(self, value: str): self._basic_option.withOutputFormat(value)

    @property
    def max_intron(self):
        """The maximum intron size for the alignment."""
        return self._basic_option.maxIntron
    @max_intron.setter
    def max_intron(self, value: int): self._basic_option.withMaxIntron(value)

    @property
    def is_dynamic(self):
        """Whether the server is dynamic."""
        return self._basic_option.isDynamic
    @is_dynamic.setter
    def is_dynamic(self, value: bool): self._basic_option.withIsDynamic(value)

    @property
    def genome(self):
        """The genome name of the server."""
        return self._basic_option.genome
    @genome.setter
    def genome(self, value: str): self._basic_option.withGenome(value)

    @property
    def genome_data_dir(self):
        """The genome data directory of the server."""
        return self._basic_option.genomeDataDir
    @genome_data_dir.setter
    def genome_data_dir(self, value: str): self._basic_option.withGenomeDataDir(value)
    # fmt: on

    @staticmethod
    def _verify_input(in_seqs: list[str | Path] | list[str] | list[Path]):
        for item in in_seqs:
            if isinstance(item, Path) and not item.exists():
                msg = f"File {item} does not exist"
                raise FileNotFoundError(msg)

            if isinstance(item, str) and ("." in item or "/" in item):
                new_item = Path(item)
                if not new_item.exists():
                    msg = f"File {item} does not exist"
                    raise FileNotFoundError(msg)

                yield new_item

            yield item

    def _query(self, in_seq: str | Path):
        basic_option = copy_client_option(self._basic_option)
        if isinstance(in_seq, Path):
            basic_option.withInName(str(in_seq)).withInSeq("").build()
        else:
            basic_option.withInSeq(str(in_seq)).withInName("").build()
        return query_server(basic_option, parse=self._parse)

    def query(self, in_seqs: INSEQS | list[str] | list[Path] | INSEQ):
        """Query the server with the specified sequences.

        Args:
            in_seqs: The sequences to query.

        Returns:
            The query results: `Bio.SearchIO.QueryResult`

        Examples:
            >>> from pxblat import Client, Server
            >>> host = "localhost"
            >>> port = 65000
            >>> seq_dir = "."
            >>> two_bit = "./test_ref.2bit"
            >>> client = Client(
            ...     host=host,
            ...     port=port,
            ...     seq_dir=seq_dir,
            ...     min_score=20,
            ...     min_identity=90,
            ... )
            >>> with Server(host, port, two_bit, can_stop=True, step_size=5) as server:
            ...     # work() assume work() is your own function that takes time to prepare something
            ...     server.wait_ready()
            ...     result1 = client.query("ATCG")
            ...     result2 = client.query("AtcG")
            ...     result3 = client.query("test_case1.fa")
            ...     result4 = client.query(["ATCG", "ATCG"])
            ...     result5 = client.query(["test_case1.fa"])
            ...     result6 = client.query(["cgTA", "test_case1.fa"])
            ...     print(result3[0]) # print result
        """
        if isinstance(in_seqs, (str, Path)):
            in_seqs = [in_seqs]

        in_seqs = list(self._verify_input(in_seqs))

        if self._wait_ready:
            wait_server_ready(
                self.host,
                self.port,
                timeout=self._wait_timeout,
                server_option=self._server_option,
            )

        results = []
        for in_seq in in_seqs:
            results.append(self._query(in_seq))

        return results
