import tempfile
from pathlib import Path
from threading import Thread
from typing import Optional

from pxblat.extc import gfClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read


def create_client_option():
    return gfClientOption()


def query_server(
    option: gfClientOption,
    host: Optional[str] = None,
    port: Optional[int] = None,
    seqname: Optional[str] = None,
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

    return ret_decode


class Client(Thread):
    def __init__(
        self,
        option: gfClientOption,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ):
        super().__init__()
        self.option = option
        self.host = host
        self.port = port
        self.result = None

    def run(self):
        ret = query_server(self.option, self.host, self.port)
        parsed_ret = read(ret, "psl")
        self.result = parsed_ret

    def get(self):
        self.join()
        return self.result

    @classmethod
    def create_option(cls):
        return create_client_option()
