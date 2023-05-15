import socket
import time
import typing
from multiprocessing import Process

from pxblat.extc import faToTwoBit
from pxblat.extc import gfServerOption
from pxblat.extc import pygetFileList
from pxblat.extc import pyqueryServer
from pxblat.extc import pystartServer
from pxblat.extc import startServer
from pxblat.extc import UsageStats


def wait_server_ready(host: str, port: int, timeout: int = 60):
    start = time.perf_counter()
    while not check_port_open(host, port):
        time.sleep(2)
        if time.perf_counter() - start > timeout:
            raise RuntimeError("wait for server ready timeout")


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
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
    useLong: bool = False,
):
    return faToTwoBit(inFiles, outFile, noMask, stripVersion, ignoreDups, useLong)


def status_server(host: str, port: int, options: gfServerOption):
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

    data = {
        " ".join(line.split()[:-1]): line.split()[-1]
        for line in data.decode("utf-8").strip().split("\n")
    }
    return data


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
):
    """Start server in blocking mode.

    Args:
        host: host name
        port: port number
        two_bit_file: two bit file path
        option: gfServeoption
        stat: statastic for server
    """
    return pystartServer(host, str(port), 1, [two_bit_file], option, stat)


def start_server_mt_nb(
    host: str,
    port: int,
    two_bit_file: str,
    option: gfServerOption,
    stat: UsageStats,
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
        args=(host, port, two_bit_file, option, stat),
        daemon=True,
    )

    process.start()
    return process
