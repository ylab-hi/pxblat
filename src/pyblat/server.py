from pathlib import Path
import typing
from multiprocessing import Process
from .utils import redirected
from .extc import gfServerOption, faToTwoBit, startServer, stopServer, statusServer


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


@redirected
def status_server(host: str, port: int, options: gfServerOption):
    return statusServer(host, str(port), options)


@redirected
def stop_server(host: str, port: int):
    return stopServer(host, str(port))


@redirected
def start_server(host: str, port: int, two_bit_file: str, options: gfServerOption):
    return startServer(host, str(port), 1, [two_bit_file], options)


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
        result = stop_server(self.host, self.port)

    def status(self):
        return status_server(self.host, self.port, self.options)

    def query(self):
        pass

    def __str__(self):
        return f"Server({self.host}, {self.port}, {self.options})"

    __repr__ = __str__

    def is_ready(self):
        return self.status().is_ok()

    def wait_ready(self):
        while not self.is_ready():
            pass
        return
