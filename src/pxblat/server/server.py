import typing
from multiprocessing import Process
from pathlib import Path

from pxblat.extc import gfServerOption
from pxblat.extc import Signal
from pxblat.extc import UsageStats

from .basic import files
from .basic import server_query
from .basic import start_server_mt
from .basic import status_server
from .basic import stop_server


def create_server_option():
    return gfServerOption()


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
        self.signal = Signal()

    def run(self):
        start_server_mt(
            self.host,
            self.port,
            self.two_bit.as_posix(),
            self.options,
            self.stat,
            self.signal,
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

    __repr__ = __str__

    def is_ready(self):
        return self.signal.isReady

    def block_until_ready(self):
        while not self.is_ready():
            pass

    @classmethod
    def create_option(cls):
        return create_server_option()
