import time
import typing
from multiprocessing import Process
from pathlib import Path

from pxblat.extc import gfServerOption
from pxblat.extc import UsageStats

from .basic import check_port_open
from .basic import files
from .basic import server_query
from .basic import start_server_mt
from .basic import status_server
from .basic import stop_server


def create_server_option():
    return gfServerOption()


def wait_server_ready(host: str, port: int, timeout: int = 60):
    start = time.perf_counter()
    while not check_port_open(host, port):
        time.sleep(2)
        if time.perf_counter() - start > timeout:
            raise RuntimeError("wait for server ready timeout")


class Server(Process):
    def __init__(
        self,
        host: str,
        port: int,
        two_bit: Path,
        options: gfServerOption,
        daemon=True,
    ):
        super().__init__(daemon=daemon)
        self.host = host
        self.port = port
        self.two_bit = two_bit
        self.options = options
        self.stat = UsageStats()
        self.is_ready = False

    def run(self):
        start_server_mt(
            self.host,
            self.port,
            self.two_bit.as_posix(),
            self.options,
            self.stat,
        )

    def stop(self):
        stop_server(self.host, self.port)

    def status(self) -> typing.Dict[str, str]:
        return status_server(self.host, self.port, self.options)

    def files(self) -> list[str]:
        return files(self.host, self.port)

    def query(self, intype: str, faName: str, isComplex: bool, isProt: bool):
        return server_query(intype, self.host, self.port, faName, isComplex, isProt)

    def __str__(self):
        return f"Server({self.host}, {self.port}, {self.options})"

    def wait_ready(self, timeout: int = 60):
        if not self.is_ready:
            wait_server_ready(self.host, self.port, timeout)
            self.is_ready = True

    @classmethod
    def create_option(cls):
        return create_server_option()

    __repr__ = __str__
