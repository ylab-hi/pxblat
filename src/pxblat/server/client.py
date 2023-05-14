import tempfile
from threading import Thread

from pxblat.extc import gfClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read


def create_client_option():
    return gfClientOption()


def query_server(host: str, port: int, option: gfClientOption):
    option.hostName = host
    option.portName = str(port)
    fafile = None

    if not option.inName and not option.inSeq:
        raise ValueError("inName and inSeq are both empty")

    if option.inSeq:
        fafile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        fafile.write(f">{fafile.inName}\n")
        fafile.write(option.inSeq)

        option.inName = fafile.name

    ret = pygfClient(option)
    parsed_ret = read(ret, "psl")

    if fafile is not None:
        fafile.close()

    return parsed_ret


class Client(Thread):
    def __init__(self, host: str, port: int, option: gfClientOption):
        super().__init__()
        self.host = host
        self.port = port
        self.option = option
        self.result = None

    def run(self):
        parsed_ret = query_server(self.host, self.port, self.option)
        self.result = parsed_ret

    def get(self):
        self.join()
        return self.result

    @classmethod
    def create_option(cls):
        return create_client_option()
