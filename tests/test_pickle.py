import pickle

import pxblat
from rich import print


def test_pickle_client_option():
    client_option = pxblat.create_client_option().withHost("localhost2").build()

    client_data = pickle.dumps(client_option)
    client_new = pickle.loads(client_data)
    assert client_new.hostName == "localhost2"


def test_pickle_server_option():
    server_option = pxblat.create_server_option().withStepSize(11).build()

    server_data = pickle.dumps(server_option)
    server_new = pickle.loads(server_data)
    print(server_new)


def test_pickle_server():
    server_option = pxblat.create_server_option().withStepSize(11).build()
    server = pxblat.Server("localhost", 1234, "tests/data/test_ref.2bit", server_option)
    server_data = pickle.dumps(server)
    server_new = pickle.loads(server_data)
    print(server_new)


def test_pickle_usestat():
    su = pxblat.UsageStats()
    su_data = pickle.dumps(su)
    pickle.loads(su_data)
