import typing
from multiprocessing import Process
from pathlib import Path
from typing import Union

from pxblat.extc import gfServerOption
from pxblat.extc import UsageStats

from .basic import files
from .basic import server_query
from .basic import start_server_mt
from .basic import status_server
from .basic import stop_server
from .basic import wait_server_ready


def create_server_option():
    return gfServerOption()


class Server(Process):
    def __init__(
        self,
        host: str,
        port: int,
        two_bit: Union[Path, str],
        options: gfServerOption,
        daemon=True,
    ):
        super().__init__(daemon=daemon)
        self.host = host
        self.port = port
        self.two_bit = two_bit
        self.options = options
        self.stat = UsageStats()
        self._is_ready = False

    def run(self):
        two_bit_file = (
            self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        )
        start_server_mt(
            self.host,
            self.port,
            two_bit_file,
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

    def is_ready(self) -> bool:
        return self._is_ready

    def wait_ready(self, timeout: int = 60):
        if not self._is_ready:
            wait_server_ready(self.host, self.port, timeout)
            self._is_ready = True

    @classmethod
    def create_option(cls):
        return create_server_option()

    __repr__ = __str__
