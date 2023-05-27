import typing as t
from contextlib import ContextDecorator
from multiprocessing import Process
from pathlib import Path
from typing import Union

from pxblat.extc import gfServerOption
from pxblat.extc import pystartServer
from pxblat.extc import UsageStats

from .basic import check_port_in_use
from .basic import files
from .basic import find_free_port
from .basic import logger
from .basic import server_query
from .basic import status_server
from .basic import stop_server
from .basic import wait_server_ready
from .status import Status


def create_server_option() -> gfServerOption:
    """
    Creates a new gfServerOption object with default values.

    Returns:
        gfServerOption: A new gfServerOption object with default values.
    """
    return gfServerOption()


class Server(ContextDecorator):
    def __init__(
        self,
        host: str,
        port: int,
        two_bit: Union[Path, str],
        option: gfServerOption,
        daemon=True,
        use_others: bool = False,
        timeout: int = 60,
        block: bool = False,
    ):
        """Initializes a gfServer object with the given parameters.

        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
            two_bit (Union[Path, str]): The path to the 2bit file or the URL of the 2bit file.
            option (gfServerOption): The options to use when starting the server.
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
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
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

                    # wait_server_ready(host, port, timeout)
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
                    self.host, str(self.port), 1, [two_bit_file], self.option, self.stat
                )
        except Exception as e:
            raise e

    def _start_nb(self):
        two_bit_file = (
            self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        )
        try:
            if check_port_in_use(self.host, self.port):
                logger.debug(f"{self.port} port in use")
                if self.use_others:
                    self._is_open = False
                    # wait_server_ready(host, port, timeout)
                else:
                    self._is_open = True
                    new_port = find_free_port(self._host, start=self.port + 1)
                    self.port = new_port
                    self._process = Process(
                        target=pystartServer,
                        args=(
                            self.host,
                            str(self.port),
                            1,
                            [two_bit_file],
                            self.option,
                            self.stat,
                        ),
                        daemon=self.daemon,
                    )
            else:
                self._is_open = True
                logger.debug(f"{self.port} port not in use")
                self._process = Process(
                    target=pystartServer,
                    args=(
                        self.host,
                        str(self.port),
                        1,
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
        """
        Starts the gfServer instance in either blocking or non-blocking mode.

        If the server is set to non-blocking mode, it will start the server in a separate process.
        If the server is set to blocking mode, it will start the server in the current process.
        """
        if not self._block:
            self._start_nb()
        else:
            self._start_b()

    def stop(self):
        """
        Stops the gfServer instance if it is running.

        This method sends a stop signal to the server process, causing it to terminate gracefully.
        """
        if self._is_open:
            stop_server(self.host, self.port)

    def status(self, instance=False) -> t.Union[t.Dict[str, str], Status]:
        """
        Retrieves the status of the gfServer instance.

        Args:
            instance (bool, optional): If True, returns a Status object. If False, returns a dictionary with status information. Defaults to False.

        Returns:
            t.Union[t.Dict[str, str], Status]: The status of the gfServer instance, either as a dictionary or a Status object.
        """
        return status_server(self.host, self.port, self.option, instance=instance)

    def files(self) -> list[str]:
        """
        Retrieves the list of files served by the gfServer instance.

        Returns:
            list[str]: A list of file names served by the gfServer instance.
        """
        return files(self.host, self.port)

    def query(self, intype: str, faName: str, isComplex: bool, isProt: bool) -> str:
        """
        Queries the gfServer instance with the given parameters.

        Args:
            intype (str): The type of input sequence. Must be one of "dna", "rna", or "protein".
            faName (str): The name of the input sequence.
            isComplex (bool): Whether the input sequence is complex.
            isProt (bool): Whether the input sequence is a protein sequence.

        Returns:
            str: The result of the query as a string.
        """
        return server_query(intype, self.host, self.port, faName, isComplex, isProt)

    def is_ready(self) -> bool:
        """
        Returns True if the server is ready to accept queries, False otherwise.

        Returns:
            bool: True if the server is ready to accept queries, False otherwise.
        """
        return self._is_ready

    def is_open(self) -> bool:
        """
        Returns True if the server is open, False otherwise.

        Returns:
            bool: True if the server is open, False otherwise.
        """
        return self._is_open

    def wait_ready(self, timeout: int = 60, restart: bool = False):
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
                    self.wait_ready(timeout * 2, restart)
                else:
                    raise RuntimeError(
                        f"Timeout for Waitting for {self.host} {self.port} server ready due to server is not opened by gfServer or need longer time to wait"
                    ) from e
            else:
                self._is_ready = True

    @classmethod
    def create_option(cls):
        """
        Creates a dictionary of options for the gfServer instance.

        Returns:
            dict: A dictionary of options for the gfServer instance.
        """
        return create_server_option()

    def __str__(self):
        return f"Server({self.host}, {self.port}, ready: {self.is_ready()} open: {self.is_open()} {self.option})"

    def __enter__(self):
        print("start server")
        self.start()
        return self

    def __exit__(self, *exc):
        print("stop server")
        self.stop()
