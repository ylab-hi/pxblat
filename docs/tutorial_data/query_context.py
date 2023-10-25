from pxblat import Client, Server

def query_context():
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

    with Server(host, port, two_bit, can_stop=True, step_size=5) as server:
        # work() assume work() is your own function that takes time to prepare something
        server.wait_ready()
        result1 = client.query("ATCG")
        result2 = client.query("AtcG")
        result3 = client.query("test_case1.fa")
        result4 = client.query(["ATCG", "ATCG"])
        result5 = client.query(["test_case1.fa"])
        result6 = client.query(["cgTA", "test_case1.fa"])
        # print results
        print(f"{result1=}")
        print(f"{result2=}")
        print(f"{result3=}")
        print(f"{result3[0]=}")
        print(f"{result3[0]=!s}")
        print(f"{result4=}")
        print(f"{result4[0]=}")
        print(f"{result5=}")
        print(f"{result6=}")

if __name__ == "__main__":
    query_context()
