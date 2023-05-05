from invoke import task
import pyblat

from pathlib import Path


def test_start_server():
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        pyblat.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.startServer("localhost", "88888", 1, [two_bit_file.as_posix()], options)


def test_server_status():
    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.statusServer("localhost", "88888", options)


def test_query_server():
    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.queryServer(
        "query", "localhost", "88888", "tests/data/test_query.fa", False, False
    )


from multiprocessing import Process


@task
def server_query(c):
    process = Process(target=test_start_server)
    process.start()
    process.join()
    print("here")
    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.queryServer(
        "query", "localhost", "88888", "tests/data/test_case1.fa", False, False
    )
    print("Stopped server")


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
        pyblat.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.startServer("localhost", "88888", 1, [two_bit_file.as_posix()], options)


@task
def pstatus_server(c, docs=False):
    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.statusServer("localhost", "88888", options)


@task
def pstop_server(c):
    pyblat.stopServer("localhost", "88888")


@task
def pquery_server(c):
    options = pyblat.gfServerOption().withCanStop(True).withStepSize(5).build()
    pyblat.queryServer(
        "query", "localhost", "88888", "tests/data/test_case1.fa", False, False
    )
