import asyncio
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pxblat
import simdjson
from invoke import task
from pxblat import extc
from rich import print

PORT = 65000


def option_stat():
    server_option = (
        extc.gfServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )

    client_option = (
        extc.gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withTSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )

    stat = extc.UsageStats()

    return server_option, client_option, stat


def test_start_server():
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    server_option, client_option, stat = option_stat()

    signal = extc.Signal()
    print(signal.isReady)
    ret = pxblat.server.start_server(
        "localhost", PORT, two_bit_file.as_posix(), server_option, stat, signal
    )
    print(signal.isReady)
    return ret


def test_start_server2():
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    server_option, client_option, stat = option_stat()

    signal = extc.Signal()
    print(signal.isReady)
    ret = pxblat.server.start_server_mt(
        "localhost", PORT, two_bit_file.as_posix(), server_option, stat, signal
    )
    print(signal.isReady)
    return ret


def test_server_status():
    server_option, client_option, stat = option_stat()
    extc.statusServer("localhost", str(PORT), server_option)


def test_query_server():
    extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    extc.queryServer(
        "query", "localhost", str(PORT), "tests/data/test_query.fa", False, False
    )


def wait_for_ready(options):
    while extc.statusServer("localhost", str(PORT), options) < 0:
        pass


@task
def cstatus_server(c, docs=False):
    c.run(f"gfServer status localhost {PORT}")


@task
def cstart_server(c):
    c.run(
        f"./bin/gfServer start localhost {PORT} tests/data/test_ref.2bit -canStop -stepSize=5 -debugLog"
    )


@task
def cstop_server(c):
    c.run(f"./bin/gfServer stop localhost {PORT}")


@task
def cquery_server(c):
    c.run(f"./bin/gfServer query localhost {PORT}  tests/data/test_case1.fa")


@task
def cclient(c):
    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} tests/data/ tests/data/test_case1.fa testc.psl"
    )


def _pclient():
    time.sleep(10)
    server_option, client_option, stat = option_stat()
    ret = extc.pygfClient(client_option)
    # print(client_option)
    print(f"{ret!r}")
    res = pxblat.read(ret, "psl")
    print(res)


@task
def pclient(c):
    start = time.perf_counter()

    with ThreadPoolExecutor(4) as executor:
        for _i in range(100):
            # _pclient()
            executor.submit(_pclient)

    print(f"time: {time.perf_counter() - start}")


def _ps():
    server_option, client_option, stat = option_stat()
    ret = pxblat.server.status_server("localhost", PORT, server_option)
    print(f"{ret}")


@task
def bpst(c):
    start = time.perf_counter()
    idx = 0

    with ThreadPoolExecutor(4) as executor:
        for _i in range(4):
            # _pclient()
            executor.submit(_ps)
            print(f"run {idx}")
            idx += 1

    print(f"time: {time.perf_counter() - start}")


@task
def bcst(c):
    # 100 0.47
    # 50 0.24
    # 1 0.01
    start = time.perf_counter()
    ret = []
    idx = 0
    for _i in range(4):
        # "gfServer status localhost {PORT}"
        t = subprocess.Popen(
            [
                "./bin/gfServer",
                "status",
                "localhost",
                str(PORT),
            ]
        )
        ret.append(t)
        print(f"run {idx}")
        idx += 1

    for i in ret:
        i.wait()

    print(f"time: {time.perf_counter() - start}")


@task
def pstart_server(c):
    res = test_start_server()
    print(f"here {res=}")


@task
def pstart_server2(c):
    res = test_start_server2()
    print(f"here {res=}")


@task
def pstatus_server(c):
    server_option, client_option, stat = option_stat()
    ret = pxblat.server.status_server("localhost", PORT, server_option)
    print(f"{ret}")


@task
def pstop_server(c):
    res = pxblat.server.stop_server("localhost", PORT)
    print(f"{res=}")


@task
def pquery_server(c):
    ret = extc.pyqueryServer(
        "query", "localhost", str(PORT), "tests/data/test_case1.fa", False, False
    )

    print(f"{ret!r}")


@task
def server(c):
    option = extc.gfServerOption().withCanStop(True).withStepSize(5).build()
    two_bit_file = Path("tests/data/test_ref.2bit")

    server = pxblat.server.Server("localhost", PORT, two_bit_file, option)
    server.start()
    server.wait_ready()

    ret = server.status()
    print(f"{ret=}")

    server.stop()
    print("python: server stopped")


@task
def add(c):
    a = 1
    print(f"before {a=}")
    extc.test_add(a)
    print(f"after {a=}")


def gfSignature():
    return b"0ddf270562684f29"


async def aread_stream(reader):
    data = b""
    while True:
        data += await reader.read(100)
        if b"end" in data:
            break
    return data


async def _asc():
    reader, writer = await asyncio.open_connection("localhost", PORT)
    writer.write(gfSignature() + b"status")
    await writer.drain()
    data = await aread_stream(reader)
    writer.close()
    await writer.wait_closed()
    return data


@task
def asc(c):
    data = asyncio.run(_asc())
    print(data)


@task
def sc(c):
    options = (
        extc.gfServerOption()
        .withCanStop(True)
        .withDebugLog(True)
        .withSyslog(True)
        .withStepSize(5)
        .build()
    )
    data = pxblat.server.status_server("localhost", PORT, options)
    print(simdjson.dumps(data, indent=4))


@task
def ls(c):
    ret = pxblat.server.files("localhost", PORT)
    print(f"{ret=}")


@task
def cp(c):
    folder = Path("./test_server")
    files = []

    for i in folder.iterdir():
        if i.is_file and i.suffix == ".cpp":
            files.append(i)

    for executor in files:
        temp = executor.parent / executor.stem
        if temp.exists():
            temp.unlink()

    complie_cmd = "g++ -I/home/ylk4626/miniconda3/envs/pxblat/include -L/home/ylk4626/miniconda3/envs/pxblat/lib -o test_server/{}  {} -luv".format

    for file in files:
        c.run(complie_cmd(file.stem, file.as_posix()))
