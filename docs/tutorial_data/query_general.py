from pxblat import Client, Server


def query_general():
    host = "localhost"
    port = 65000
    seq_dir = "."
    two_bit = "./test_ref.2bit"

    client = Client(
        host=host,
        port=port,
        seq_dir=seq_dir,
        min_score=20,
        min_identity=90,
    )

    server = Server(host, port, two_bit, can_stop=True, step_size=5)
    server.start()
    # work() assume work() is your own function that takes time to prepare something
    server.wait_ready()
    result1 = client.query(["actg", "test_case1.fa"])
    # another_work() assume the func is your own function that takes time
    result2 = client.query("test_case1.fa")
    server.stop()

    print(f"{result1=}")
    print(f"{result2=}")


if __name__ == "__main__":
    query_general()
