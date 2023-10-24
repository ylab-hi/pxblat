from __future__ import annotations

import errno
import socket
import time
import warnings
from collections import Counter
from multiprocessing import Process

from deprecated import deprecated  # type: ignore

from pxblat.extc import (
    ServerOption,
    UsageStats,
    pygetFileList,
    pyqueryServer,
    pystartServer,
    startServer,
)

from .status import Status

MAX_PORT = 65535


def check_port_in_use(host: str, port: int, tries: int = 3) -> bool:
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

    Example:
        >>> check_port_in_use('localhost', 8080)
        True
    """
    res = [_check_port_in_use_by_connect(host, port) for _ in range(tries)]
    counter = Counter(res)
    return counter[True] > counter[False]


def _check_port_in_use_by_status(
    host: str,
    port: int,
    server_option: ServerOption,
) -> bool:
    """Check the port is in use by status_server.

    Args:
        host: host name
        port: port number
        server_option: server option for the opening server

    Returns:
        True if the port is in use

    Note:
        The server option can be default value and will not influence result
        Also, it can detect if the port is opened by gfServer as well
    """
    return check_server_status(host, port, server_option)


def _check_port_in_use_by_connect(host: str, port: int):
    """Check the port is in use by connect to the port.

    Args:
        host: host name
        port: port number

    Returns:
        True if the port is in use

    Note:
        The function has same feature as `_check_port_in_use_by_status`
        It check the port if it is in use by connect to the port.
        But it cannot detect if the port is opened by gfServer
    """
    return check_port_open(host, port)


@deprecated(
    reason="The func will generate false alarm. Please use `_check_port_in_use_by_status` or  `_check_port_in_use_by_connect` instead",
)
def _check_port_in_use_by_bind(host: str, port: int):
    """Check the port is in use by bind to the port.

    Args:
        host: host name
        port: port number

    Returns:
        True if the port is in use

    Note:
        The function check the port if it is in use by bind to the port.
        It is not reliable as ``_check_port_in_use_by_connect`` or
        ``_check_port_in_use_by_status``

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            return True

        raise e

    s.close()
    return False


def wait_server_ready(
    host: str,
    port: int,
    timeout: int = 60,
    server_option=None,
) -> None:
    """Wait for a server to become ready by checking if a given port is open or if a specific server status is reached.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to check for open status.
        timeout (int, optional): The maximum number of seconds to wait for the server to become ready. Defaults to 60.
        server_option (str, optional): The specific server status to check for. If None, the function will check for an open port. Defaults to None.

    Raises:
        RuntimeError: If the server does not become ready within the specified timeout.

    Returns:
        None
    """
    start = time.perf_counter()

    if server_option is None:
        warnings.warn(
            "Use `check_server_status` instead of `check_port_open` when wait for ready",
            stacklevel=1,
        )
        while not check_port_open(host, port):
            time.sleep(1)
            if time.perf_counter() - start > timeout:
                msg = "wait for server ready timeout"
                raise RuntimeError(msg)
    else:
        while not check_server_status(host, port, server_option):
            time.sleep(1)
            if time.perf_counter() - start > timeout:
                msg = "wait for server ready timeout"
                raise RuntimeError(msg)


def check_server_status(
    host: str,
    port: int,
    server_option: ServerOption,
) -> bool:
    """Check the status of a server by attempting to connect to it using the specified host, port, and gfserver_option.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to use when attempting to connect to the server.
        server_option (ServerOption): The gfserver option to use when attempting to connect to the server.

    Returns:
        bool: True if the server is running and accepting connections, False otherwise.

    Raises:
        ConnectionRefusedError: If the server is not running or is not accepting connections.

    Example:
        >>> check_server_status('localhost', 8080, ServerOption)
        True
    """
    try:
        status_server(host, port, server_option)
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


def _gfSignature() -> str:
    """Get the gfSignature."""
    return "0ddf270562684f29"


def status_server(
    host: str,
    port: int,
    server_option: ServerOption,
    *,
    instance=False,
) -> Status | dict[str, str]:
    """Get the status of a running server.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to use when attempting to connect to the server.
        server_option (ServerOption): The gfserver option to use when attempting to connect to the server.
        instance (bool, optional): If True, return a Status object instead of a dictionary. Defaults to False.

    Returns:
        Union[Status, Dict[str, str]]: A dictionary or Status object containing the status information for the server.

    Example:
        >>> status_server('localhost', 8080, ServerOption, instance=True)
        Status(uptime='0', queries='0', sequences='0', bytes='0', memory='0', threads='0', connections='0')
    """
    if not server_option.genome:
        message = f"{_gfSignature()}status".encode()
    else:
        temp = "transInfo" if server_option.trans else "untransInfo"
        message = f"{_gfSignature()}{temp} {server_option.genome} {server_option.genomeDataDir}".encode()

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

    data_dict = {" ".join(line.split()[:-1]): line.split()[-1] for line in data.decode("utf-8").strip().split("\n")}

    if instance:
        return Status.from_dict(data_dict)

    return data_dict


def stop_server(host: str, port: int):
    """Stop a running server.

    Args:
        host (str): The hostname or IP address of the server to stop.
        port (int): The port number to use when attempting to connect to the server.

    Returns:
        None

    This function stops a running server by sending a "quit" message to the server. The function takes the hostname and port number
    of the server as arguments. The function returns None.

    Example:
        >>> stop_server('localhost', 8080)
    """
    message = f"{_gfSignature()}quit".encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message)


def files(host: str, port: int) -> list[str]:
    """Get a list of files available on the server.

    Args:
        host (str): The hostname or IP address of the server to check.
        port (int): The port number to use when attempting to connect to the server.

    Returns:
        List[str]: A list of file names available on the server.

    This function retrieves a list of files available on the server by sending a "files" message to the server. The function takes
    the hostname and port number of the server as arguments. The function returns a list of file names available on the server.

    Example:
        >>> files('localhost', 8080)
        ['file1', 'file2', 'file3']
    """
    ret_str = pygetFileList(host, str(port))
    if ret_str == "":
        raise ValueError
    return [file for file in ret_str.split("\n") if file]


def server_query(
    intype: str,
    host: str,
    port: int,
    faName: str,
    *,
    isComplex: bool,
    isProt: bool,
):
    """Query a running server with a sequence.

    Args:
        intype (str): The type of input sequence. Must be one of 'dna', 'rna', or 'protein'.
        host (str): The hostname or IP address of the server to query.
        port (int): The port number to use when attempting to connect to the server.
        faName (str): The name of the input sequence.
        isComplex (bool): Whether the input sequence is complex.
        isProt (bool): Whether the input sequence is a protein sequence.

    Returns:
        str: The result of the query.

    This function queries a running server with a sequence by sending a "query" message to the server. The function takes the
    type of input sequence, hostname, port number, sequence name, and whether the sequence is complex or a protein sequence as
    arguments. The function returns the result of the query as a string.

    Example:
        >>> server_query('dna', 'localhost', 8080, 'sequence1', False, False)
        'result1'
    """
    return pyqueryServer(intype, host, str(port), faName, isComplex, isProt)


def start_server(
    host: str,
    port: int,
    two_bit_file: str,
    server_option: ServerOption,
    stat: UsageStats,
):
    """Start a server in blocking mode.

    Args:
        host (str): The hostname or IP address to bind the server to.
        port (int): The port number to bind the server to.
        two_bit_file (str): The path to the 2bit file to use for the server.
        server_option (ServerOption): The options to use for the server.
        stat (UsageStats): The usage statistics for the server.

    Returns:
        None

    This function starts a server in blocking mode by calling the pystartServer function with the given arguments. The function
    takes the hostname, port number, 2bit file path, server options, and usage statistics as arguments. The function returns None.

    Example:
        >>> start_server('localhost', 8080, '/path/to/2bit/file', ServerOption, UsageStats())
    """
    return startServer(host, str(port), 1, [two_bit_file], server_option, stat)


def start_server_mt(
    host: str,
    port: int,
    two_bit_file: str,
    server_option: ServerOption,
    stat: UsageStats,
    *,
    use_others: bool = False,
    try_new_port: bool = True,
):
    """Starts a server on a new thread.

    This function attempts to start a server on the given host and port, using the provided .2bit file, options, and usage stats.
    If the port is in use, it either waits for the server to be ready, tries a new port, or raises an error, depending on the options.

    Args:
        host (str): The hostname or IP address to start the server on.
        port (int): The initial port number to try to start the server on.
        two_bit_file (str): The .2bit file to use for the server.
        server_option (ServerOption): The options to use when starting the server.
        stat (UsageStats): The usage stats to use for the server.
        use_others (bool, optional): Whether to use the port even if it is already in use. Defaults to False.
        try_new_port (bool, optional): Whether to try a new port if the initial port is in use. Defaults to True.

    Raises:
        ValueError: If the port is in use and neither 'use_others' nor 'try_new_port' is True.
        Exception: If there is any other error in starting the server.
    """
    try:
        if check_port_in_use(host, port):
            if use_others:
                pass
            elif try_new_port:
                port = find_free_port(host, start=port + 1)
                pystartServer(host, str(port), 1, [two_bit_file], server_option, stat)
            else:
                msg = f"The port {port} is used"
                raise ValueError(msg)
        else:
            pystartServer(host, str(port), 1, [two_bit_file], server_option, stat)
    except Exception as e:
        raise e


def start_server_mt_nb(
    host: str,
    port: int,
    two_bit_file: str,
    server_option: ServerOption,
    stat: UsageStats,
    *,
    use_others: bool = False,
    try_new_port: bool = True,
) -> Process:
    """Starts a server on a new thread and immediately returns a Process object.

    This function calls `start_server_mt` to start a server on the given host and port, using the provided .2bit file, options, and usage stats,
    in a new thread, and immediately returns a Process object for the new thread.

    Args:
        host (str): The hostname or IP address to start the server on.
        port (int): The initial port number to try to start the server on.
        two_bit_file (str): The .2bit file to use for the server.
        server_option (ServerOption): The options to use when starting the server.
        stat (UsageStats): The usage stats to use for the server.
        use_others (bool, optional): Whether to use the port even if it is already in use. Defaults to False.
        try_new_port (bool, optional): Whether to try a new port if the initial port is in use. Defaults to True.

    Returns:
        Process: A Process object for the newly started thread.
    """
    process = Process(
        target=start_server_mt,
        args=(
            host,
            port,
            two_bit_file,
            server_option,
            stat,
        ),
        kwargs={
            "use_others": use_others,
            "try_new_port": try_new_port,
        },
        daemon=True,
    )

    process.start()
    return process


def find_free_port(host: str, start: int, end: int = MAX_PORT) -> int:
    """Find an available port in the range of [start, end).

    Args:
        host: Hostname
        start: Start port number
        end: End port number.
    """
    if start > end:
        raise ValueError

    for port in range(start, end):
        try:
            if not check_port_in_use(host, port):
                return port
        except OSError as e:
            raise e
    msg = f"Cannot find available port in range [{start}, {end}]"
    raise RuntimeError(msg)
