import typing
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


def create_server_option():
    return gfServerOption()


class Server:
    def __init__(
        self,
        host: str,
        port: int,
        two_bit: Union[Path, str],
        option: gfServerOption,
        daemon=True,
        use_others: bool = False,
        timeout: int = 60,
    ):
        self._host = host
        self._port = port
        self.two_bit = two_bit
        self.option = option
        self.stat = UsageStats()
        self.use_others = use_others
        self.timeout = timeout
        self.daemon = daemon

        self._is_ready = False
        self._is_open = False

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

    def start(self):
        two_bit_file = (
            self.two_bit if isinstance(self.two_bit, str) else self.two_bit.as_posix()
        )
        try:
            if check_port_in_use(self._host, self.port):
                logger.info(f"{self.port} port in use")
                if self.use_others:
                    pass
                    # wait_server_ready(host, port, timeout)
                    # status_server(host, port, option)
                else:
                    new_port = find_free_port(self._host, start=self.port + 1)
                    self.port = new_port
                    self._is_open = True
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
                logger.info(f"{self.port} port not in use")

                self._is_open = True
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

    def stop(self):
        if self._is_open:
            stop_server(self.host, self.port)

    def status(self) -> typing.Dict[str, str]:
        return status_server(self.host, self.port, self.option)

    def files(self) -> list[str]:
        return files(self.host, self.port)

    def query(self, intype: str, faName: str, isComplex: bool, isProt: bool):
        return server_query(intype, self.host, self.port, faName, isComplex, isProt)

    def is_ready(self) -> bool:
        return self._is_ready

    def wait_ready(self, timeout: int = 60):
        if not self._is_ready:
            wait_server_ready(self.host, self.port, timeout)
            self._is_ready = True

    @classmethod
    def create_option(cls):
        return create_server_option()

    def __str__(self):
        return (
            f"Server({self.host}, {self.port}, ready: {self.is_ready()} {self.option})"
        )
