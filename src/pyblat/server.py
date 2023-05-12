import socket
import typing
from multiprocessing import Process
from pathlib import Path

from .extc import faToTwoBit
from .extc import gfServerOption
from .extc import pygetFileList
from .extc import pyqueryServer
from .extc import startServer
from .extc import UsageStats
from .utils import redirected


def gfSignature() -> str:
    return "0ddf270562684f29"


@redirected
def fa_to_two_bit(
    inFiles: typing.List[str],
    outFile: str,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
    useLong: bool = False,
):
    return faToTwoBit(inFiles, outFile, noMask, stripVersion, ignoreDups, useLong)


# @redirected
# def status_server(host: str, port: int, options: gfServerOption):
#     return statusServer(host, str(port), options)


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

    print(f"{data!r}")

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


# d::string pyqueryServer(std::string &type, std::string &hostName, std::string &portName, std::string &faName, bool complex, bool isProt)
def query_server(
    intype: str, host: str, port: int, faName: str, isComplex: bool, isProt: bool
):
    re_str = pyqueryServer(intype, host, str(port), faName, isComplex, isProt)
    return re_str


# @redirected
def start_server(
    host: str, port: int, two_bit_file: str, option: gfServerOption, stat: UsageStats
):
    return startServer(host, str(port), 1, [two_bit_file], option, stat)


class Server:
    def __init__(self, host: str, port: int, two_bit: Path, options: gfServerOption):
        self.host = host
        self.port = port
        self.two_bit = two_bit
        self.options = options
        self.process_handle = None

    def start(self):
        self.process_handle = Process(
            target=startServer,
            args=(
                self.host,
                str(self.port),
                1,
                [self.two_bit.as_posix()],
                self.options,
            ),
        )
        self.process_handle.start()

    def stop(self):
        stop_server(self.host, self.port)

    def status(self) -> typing.Dict[str, str]:
        return status_server(self.host, self.port, self.options)

    def files(self) -> list[str]:
        return files(self.host, self.port)

    def query(self, intype: str, faName: str, isComplex: bool, isProt: bool):
        return query_server(intype, self.host, self.port, faName, isComplex, isProt)

    def __str__(self):
        return f"Server({self.host}, {self.port}, {self.options})"

    __repr__ = __str__

    def is_ready(self):
        return self.status().is_ok()

    def wait_ready(self):
        while not self.is_ready():
            pass
