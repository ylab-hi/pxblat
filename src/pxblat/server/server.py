from __future__ import annotations

import typing as t
from contextlib import ContextDecorator
from multiprocessing import Process

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
    from pathlib import Path

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
    """
    return ServerOption()


class Server(ContextDecorator):
    """A context manager and decorator for managing a server process.

    This class can be used as a context manager or decorator to manage a server process. It starts the server with the given
    options, and can run it as a daemon process or block until it is ready.

    Attributes:
        host (str): The hostname or IP address to bind the server to.
        port (int): The port number to bind the server to.
        two_bit (Union[Path, str]): The path to the 2bit file or the URL of the 2bit file.
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
        option: ServerOption,
        *,
        daemon=True,
        use_others: bool = False,
        timeout: int = 60,
        block: bool = False,
    ) -> None:
        """Initializes a gfServer object with the given parameters.

        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
            two_bit (Union[Path, str]): The path to the 2bit file or the URL of the 2bit file.
            option (ServerOption): The options to use when starting the server.
            daemon (bool, optional): Whether to run the server as a daemon process. Defaults to True.
            use_others (bool, optional): Whether to allow other users to access the server. Defaults to False.
            timeout (int, optional): The number of seconds to wait for the server to start. Defaults to 60.
            block (bool, optional): Whether to block until the server is ready. Defaults to False.

        Raises:
            ValueError: If the given two_bit file or URL is invalid.
            OSError: If there is an error starting the server process.

        Returns:
            None

        """
        self._host = host
        self._port = port

        self.two_bit = two_bit
        self.option = option
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
        two_bit_file = (
            self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        )
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
        two_bit_file = (
            self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        )
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

    def start(self):
        """Starts the gfServer instance in either blocking or non-blocking mode.

        If the server is set to non-blocking mode, it will start the server in a separate process.
        If the server is set to blocking mode, it will start the server in the current process.
        """
        if not self._block:
            self._start_nb()
        else:
            self._start_b()

    def stop(self):
        """Stops the gfServer instance if it is running.

        This method sends a stop signal to the server process, causing it to terminate gracefully.
        """
        if self._is_open:
            stop_server(self.host, self.port)

        if self._process is not None:
            self._process.terminate()

    def status(self, *, instance=False) -> dict[str, str] | Status:
        """Retrieves the status of the gfServer instance.

        Args:
            instance (bool, optional): If True, returns a Status object. If False, returns a dictionary with status information. Defaults to False.

        Returns:
            t.Union[t.Dict[str, str], Status]: The status of the gfServer instance, either as a dictionary or a Status object.
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

    @staticmethod
    def create_option() -> ServerOption:
        """Creates a ServerOption for the gfServer instance.

        Returns:
            ServerOption: A class that hold options for the gfServer instance.
        """
        return create_server_option()

    def __str__(self) -> str:
        """Return server option as a string."""
        return f"Server({self.host}, {self.port}, ready: {self.is_ready()} open: {self.is_open()} {self.option})"

    def __enter__(self):
        """Starts the gfServer instance in blocking mode when used as a context manager."""
        self.start()
        return self

    def __exit__(self, *exc):
        """Stops the gfServer."""
        self.stop()
