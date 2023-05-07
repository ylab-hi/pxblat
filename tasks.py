from pathlib import Path

import pyblat
from invoke import task
from pyblat import extc


def test_start_server():
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    options = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    extc.startServer("localhost", "88888", 1, [two_bit_file.as_posix()], options)


def test_server_status():
    options = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    extc.statusServer("localhost", "88888", options)


def test_query_server():
    extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    extc.queryServer(
        "query", "localhost", "88888", "tests/data/test_query.fa", False, False
    )


def wait_for_ready(options):
    while extc.statusServer("localhost", "88888", options) < 0:
        pass


@task
def server_query(c):
    two_bit_file = Path("tests/data/test_ref.2bit")
    options = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    res1 = pyblat.server.start_server(
        "localhost", 88888, two_bit_file.as_posix(), options
    )

    while True:
        res2 = pyblat.server.status_server("localhost", 88888, options)
        if res2.returncode >= 0:
            break

    print("server is ready")

    pyblat.server.stop_server("localhost", 88888)
    print("stopping server")
    res1.result().join()

    print(f"{res1.stdout=}")
    print(f"{res1.stderr=}")

    # extc.stopServer("localhost", "88888")


@task
def cstatus_server(c, docs=False):
    c.run("gfServer status localhost 88888")


@task
def cstart_server(c):
    c.run(
        "./bin/gfServer start localhost 88888 tests/data/test_ref.2bit -canStop -stepSize=5"
    )


@task
def cstop_server(c):
    c.run("./bin/gfServer stop localhost 88888")


@task
def cquery_server(c):
    c.run("./bin/gfServer query localhost 88888  tests/data/test_case1.fa")


@task
def pstart_server(c):
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    options = extc.gfServerOption().withCanStop(True).withStepSize(5).build()

    res = pyblat.server.start_server(
        "localhost", 88888, two_bit_file.as_posix(), options
    )

    print(f"here {res=}")


@task
def pstatus_server(c):
    options = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    ret = pyblat.server.status_server("localhost", 88888, options)
    print(f"{ret}")


@task
def pstop_server(c):
    res = pyblat.server.stop_server("localhost", 88888)
    print(f"{res=}")


@task
def pquery_server(c):
    extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    extc.queryServer(
        "query", "localhost", "88888", "tests/data/test_case1.fa", False, False
    )


@task
def server(c):
    option = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    two_bit_file = Path("tests/data/test_ref.2bit")

    server = pyblat.server.Server("localhost", 88888, two_bit_file, option)
    server.start()
    server.wait_ready()

    ret = server.status()
    print(f"{ret=}")

    server.stop()
    print("python: server stopped")


@task
def stdout(c):
    # Call a function from the shared library that prints to stdout
    # extc.test_stdout()
    pass
