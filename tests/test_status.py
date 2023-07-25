from pxblat.server import Status


def test_construct_status_from_dict(expected_status, expected_status_instance):
    instance = Status.from_dict(expected_status)
    assert instance == expected_status_instance


def test_construct_status(start_server, expected_status_instance):
    status = start_server.status(instance=True)
    assert status == expected_status_instance
