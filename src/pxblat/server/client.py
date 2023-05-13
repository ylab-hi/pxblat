from threading import Thread

from pxblat.extc import gfClientOption
from pxblat.extc import pygfClient
from pxblat.parser import read


def create_client_option():
    return gfClientOption()


def query_server(host: str, port: int, option: gfClientOption):
    option.hostName = host
    option.portName = str(port)
    ret = pygfClient(option)
    parsed_ret = read(ret, "psl")
    return parsed_ret


class Client(Thread):
    def __init__(self, host: str, port: int, option: gfClientOption):
        super().__init__()
        self.host = host
        self.port = port
        self.option = option
        self.result = None

    def _check_option(self):
        self.option.hostName = self.host
        self.option.portName = str(self.port)

    def run(self):
        self._check_option()
        ret = pygfClient(self.option)
        parsed_ret = read(ret, "psl")
        self.result = parsed_ret

    def get(self):
        self.join()
        return self.result

    @classmethod
    def create_option(cls):
        return create_client_option()
