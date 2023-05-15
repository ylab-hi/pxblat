import tempfile
from pathlib import Path
from threading import Thread
from typing import Optional

from pxblat.extc import gfClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read

from .basic import wait_server_ready


def create_client_option():
    return gfClientOption()


def query_server(
    option: gfClientOption,
    host: Optional[str] = None,
    port: Optional[int] = None,
    seqname: Optional[str] = None,
    parse: bool = True,
):
    if host is not None:
        option.hostName = host

    if port is not None:
        option.portName = str(port)

    fafile = None
    if not option.inName and not option.inSeq:
        raise ValueError("inName and inSeq are both empty")

    if option.inSeq:
        fafile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        seqname = fafile.name if seqname is None else seqname
        fafile.write(f">{seqname}\n")
        fafile.write(option.inSeq)
        fafile.close()

        option.inName = fafile.name

    # return bytes
    ret = pygfClient(option)

    try:
        ret_decode = ret.decode().rsplit("\n", 1)[0]  # type: ignore
    except UnicodeDecodeError:
        ret_decode = ret.decode("latin-1").rsplit("\n", 1)[0]  # type: ignore

    if fafile is not None:
        Path(fafile.name).unlink()

    if parse:
        return read(ret_decode, "psl")

    return ret_decode


class Client(Thread):
    def __init__(
        self,
        option: gfClientOption,
        host: Optional[str] = None,
        port: Optional[int] = None,
        wait_ready: bool = False,
    ):
        super().__init__()
        self.option = option
        self._host = host
        self._port = port
        self.result = None
        self.wait_ready = wait_ready
        self.check_host_port()

    def run(self):
        if self.wait_ready:
            wait_server_ready(self.host, self.port)

        ret = query_server(self.option, self.host, self.port)
        parsed_ret = read(ret, "psl")  # type: ignore
        self.result = parsed_ret

    def get(self):
        self.join()
        return self.result

    @property
    def host(self):
        if self._host is None:
            return self.option.hostName

        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self):
        if self._port is None:
            return int(self.option.portName)

        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @classmethod
    def create_option(cls):
        return create_client_option()

    def check_host_port(self):
        if not self.host and self.port == 0:
            raise ValueError("host and port are both empty")
