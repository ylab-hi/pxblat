import errno
import socket
import time
import typing as t
import warnings
from collections import Counter
from multiprocessing import Process

from deprecated import deprecated  # type: ignore
from pxblat.extc import faToTwoBit
from pxblat.extc import gfServerOption
from pxblat.extc import pygetFileList
from pxblat.extc import pyqueryServer
from pxblat.extc import pystartServer
from pxblat.extc import startServer
from pxblat.extc import UsageStats

from .status import Status
from .utils import logger

DEFAULT_PORT = 65000


def check_host_port(host: str, port: int) -> None:
    """Check if the given host and port are valid.

    Args:
        host (str): The host to check.
        port (int): The port to check.

    Returns:
        None

    Raises:
        RuntimeError: If the host is not a string or the port is not an integer.

    This function checks if the given host and port are valid. The host must be a string and the port must be an integer.
    If either of these conditions are not met, a RuntimeError is raised with an appropriate error message.

    Example:
        >>> check_host_port("localhost", 8080)
        None
    """
    if not isinstance(host, str):
        raise RuntimeError("host must be str")

    if not isinstance(port, int):
        raise RuntimeError("port must be number")


def check_port_in_use(host: str, port: int = DEFAULT_PORT, tries: int = 3) -> bool:
    """Check if a given port on a host is in use.

    Args:
        host (str): The hostname or IP address of the host to check.
        port (int, optional): The port number to check. Defaults to DEFAULT_PORT.
        tries (int, optional): The number of times to attempt the check. Defaults to 3.

    Returns:
        bool: True if the port is in use, False otherwise.

    Raises:
        TypeError: If the host argument is not a string.
        ValueError: If the port argument is not a valid port number.

    This function attempts to connect to the specified host and port using the socket library. It will attempt the connection
    a number of times specified by the tries argument. If the connection is successful, it will return True, indicating that
    the port is in use. If the connection fails, it will return False.

    If the host argument is not a string, a TypeError will be raised. If the port argument is not a valid port number, a
    ValueError will be raised.

    Example usage:
    >>> check_port_in_use('localhost', 8080)
    True
    """
    res = [_check_port_in_use_by_connect(host, port) for _ in range(tries)]
    counter = Counter(res)
    logger.debug(f"{res}")
    return counter[True] > counter[False]


def _check_port_in_use_by_status(
    host: str, port: int, gfserver_option: gfServerOption
) -> bool:
    """Check the port is in use by status_server

    Args:
        host: host name
        port: port number
        gfserver_option: server option for the opening server

    Returns:
        True if the port is in use

    note:
        The server option can be default value and will not influence result
        Also, it can detect if the port is opened by gfServer as well
    """
    logger.debug(f"check port {host}:{port}")
    return check_server_status(host, port, gfserver_option)


def _check_port_in_use_by_connect(host: str, port: int):
    """Check the port is in use by connect to the port

    Args:
        host: host name
        port: port number

    Returns:
        True if the port is in use

    note:
        The function has same feature as `_check_port_in_use_by_status`
        It check the port if it is in use by connect to the port.
        But it cannot detect if the port is opened by gfServer
    """
    return check_port_open(host, port)


@deprecated(
    reason="The func will generate false alarm. Please use `_check_port_in_use_by_status` or  `_check_port_in_use_by_connect` instead"
)
def _check_port_in_use_by_bind(host: str, port: int = DEFAULT_PORT):
    """Check the port is in use by bind to the port

    Args:
        host: host name
        port: port number

    Returns:
        True if the port is in use

    note:
        The function check the port if it is in use by bind to the port.
        It is not reliable as `_check_port_in_use_by_connect` or `_check_port_in_use_by_status`
    """
    logger.debug(f"check port {host}:{port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except socket.error as e:
        logger.debug(f"port {host}:{port} is in use {e}")
        if e.errno == errno.EADDRINUSE:
            return True

        raise e

    s.close()
    return False


def wait_server_ready(
    host: str, port: int, timeout: int = 60, gfserver_option=None
) -> None:
    """Wait for a server to become ready by checking if a given port is open or if a specific server status is reached.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to check for open status.
        timeout (int, optional): The maximum number of seconds to wait for the server to become ready. Defaults to 60.
        gfserver_option (str, optional): The specific server status to check for. If None, the function will check for an open port. Defaults to None.

    Raises:
        RuntimeError: If the server does not become ready within the specified timeout.

    Returns:
        None
    """
    start = time.perf_counter()

    if gfserver_option is None:
        warnings.warn(
            "Use `check_server_status` instead of `check_port_open` when wait for ready",
            stacklevel=1,
        )
        while not check_port_open(host, port):
            time.sleep(1)
            if time.perf_counter() - start > timeout:
                raise RuntimeError("wait for server ready timeout")
    else:
        while not check_server_status(host, port, gfserver_option):
            time.sleep(1)
            if time.perf_counter() - start > timeout:
                raise RuntimeError("wait for server ready timeout")


def check_server_status(
    host: str,
    port: int,
    gfserver_option: gfServerOption,
) -> bool:
    """Check the status of a server by attempting to connect to it using the specified host, port, and gfserver_option.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to use when attempting to connect to the server.
        gfserver_option (gfServerOption): The gfserver option to use when attempting to connect to the server.

    Returns:
        bool: True if the server is running and accepting connections, False otherwise.

    Raises:
        ConnectionRefusedError: If the server is not running or is not accepting connections.

    Example:
        >>> check_server_status('localhost', 8080, gfServerOption)
        True
    """
    try:
        status_server(host, port, gfserver_option)
    except ConnectionRefusedError:
        return False
    else:
        return True


def check_port_open(host: str, port: int) -> bool:
    """Check the port is open and can accept message or not.

    Args:
        host: Hostname
        port: Port number

    Returns:
        True if the port is open and can accept message, otherwise False.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def gfSignature() -> str:
    return "0ddf270562684f29"


def fa_to_two_bit(
    inFiles: t.List[str],
    outFile: str,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
    useLong: bool = False,
):
    return faToTwoBit(inFiles, outFile, noMask, stripVersion, ignoreDups, useLong)


def status_server(
    host: str, port: int, options: gfServerOption, instance=False
) -> t.Union[Status, t.Dict[str, str]]:
    if not options.genome:
        message = f"{gfSignature()}status".encode()
    else:
        temp = "transInfo" if options.trans else "untransInfo"
        message = (
            f"{gfSignature()}{temp} {options.genome} {options.genomeDataDir}".encode()
        )

    data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message)
        while True:
            data += s.recv(1024)
            if b"end" in data:
                break

        mapping = {
            b"\x00": b"\n",
            b"\x03": b"\n",
            b"\x04": b"\n",
            b"\x07": b"\n",
            b"\x08": b"\n",
            b"\x11": b"\n",
            b"\x10": b"\n",
            b"\x0b": b"\n",
            b"\x0c": b"\n",
            b"\x0e": b"\n",
            b"\x0f": b"\n",
            b"\t": b"\n",
            b"end": b"",
        }

    for k, v in mapping.items():
        data = data.replace(k, v)

    data_dict = {
        " ".join(line.split()[:-1]): line.split()[-1]
        for line in data.decode("utf-8").strip().split("\n")
    }

    if instance:
        return Status.from_dict(data_dict)

    return data_dict


def stop_server(host: str, port: int):
    message = f"{gfSignature()}quit".encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message)


def files(host: str, port: int) -> list[str]:
    ret_str = pygetFileList(host, str(port))
    assert ret_str, "ret_str cannot be empty"
    return [file for file in ret_str.split("\n") if file]


def server_query(
    intype: str, host: str, port: int, faName: str, isComplex: bool, isProt: bool
):
    re_str = pyqueryServer(intype, host, str(port), faName, isComplex, isProt)
    return re_str


def start_server(
    host: str,
    port: int,
    two_bit_file: str,
    option: gfServerOption,
    stat: UsageStats,
):
    return startServer(host, str(port), 1, [two_bit_file], option, stat)


def start_server_mt(
    host: str,
    port: int,
    two_bit_file: str,
    option: gfServerOption,
    stat: UsageStats,
    use_others: bool = False,
    timeout: int = 60,
    try_new_port: bool = True,
):
    """Start server in blocking mode.

    Args:
        host: host name
        port: port number
        two_bit_file: two bit file path
        option: gfServeoption
        stat: statastic for server
    """
    try:
        if check_port_in_use(host, port):
            if use_others:
                pass
                # wait_server_ready(host, port, timeout)
                # status_server(host, port, option)
            elif try_new_port:
                port = find_free_port(host, start=port + 1)
                pystartServer(host, str(port), 1, [two_bit_file], option, stat)
            else:
                raise ValueError(f"The port {port} is used")
        else:
            pystartServer(host, str(port), 1, [two_bit_file], option, stat)
    except Exception as e:
        raise e


def start_server_mt_nb(
    host: str,
    port: int,
    two_bit_file: str,
    option: gfServerOption,
    stat: UsageStats,
    use_others: bool = False,
    timeout: int = 60,
    try_new_port: bool = True,
) -> Process:
    """Start server in non-blocking mode.

    Args:
        host: host name
        port: port number
        two_bit_file: two bit file path
        option: gfServeoption
        stat: statastic for server

    Returns:
        Process: a process object
    """
    process = Process(
        target=start_server_mt,
        args=(
            host,
            port,
            two_bit_file,
            option,
            stat,
            use_others,
            timeout,
            try_new_port,
        ),
        daemon=True,
    )

    process.start()
    return process


def find_free_port(host: str, start: int = DEFAULT_PORT, end: int = 65535) -> int:
    """Find an available port in the range of [start, end].
    Args:
        host: Hostname
        start: Start port number
        end: End port number
    """
    assert start < end

    for port in range(start, end):
        try:
            if not check_port_in_use(host, port):
                return port
        except socket.error as e:
            raise e
    raise RuntimeError(f"Cannot find available port in range [{start}, {end}]")
