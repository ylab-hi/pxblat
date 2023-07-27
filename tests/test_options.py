from pxblat import ClientOption, copy_client_option


def test_client_option_copy(port):
    client_option = (
        ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(port))
        .withSeqDir("tests/data/")
    )

    assert client_option.inName == ""

    correct_copy = copy_client_option(client_option)

    pointer_copy = client_option

    client_option.withInName("tests/data/test_case1.fa")

    assert client_option.inName == "tests/data/test_case1.fa"
    assert correct_copy.inName == ""
    assert pointer_copy.inName == "tests/data/test_case1.fa"
