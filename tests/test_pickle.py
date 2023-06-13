from pxblat.extc import ClientOption, set_state


def test_set_state_for_client():
    client_option = ClientOption().withHost("localhost2").build()
    new_client_option = ClientOption()
    set_state(new_client_option, client_option.__getstate__())
    assert new_client_option.hostName == client_option.hostName
