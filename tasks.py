import asyncio
import subprocess
import threading
import time
import typing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from pathlib import Path

import pxblat
import simdjson
from invoke.tasks import task
from pxblat import extc
from pxblat.extc import pygfClient
from pxblat.server import ClientThread
from pxblat.server import Server
from pxblat.server import start_server_mt_nb
from pxblat.server import status_server
from pxblat.server import wait_server_ready
from rich import print

PORT = 65000


def get_files_by_suffix(
    path: typing.Union[Path, str], suffix: typing.List[str]
) -> typing.Iterator[Path]:
    """Get bindings."""
    if isinstance(path, str):
        path = Path(path)

    for file in path.iterdir():
        if file.is_dir():
            yield from get_files_by_suffix(file, suffix)
        if file.suffix in suffix:
            yield file


def worker():
    return threading.current_thread().ident


def dummy_work(num):
    for i in range(num):
        print(f"{worker()} working for {i}")
        time.sleep(1)


def option_stat():
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(1).build()
    )

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir("tests/data/")
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

    ret = pxblat.server.start_server(
        "localhost", PORT, two_bit_file.as_posix(), server_option, stat
    )
    return ret


def test_start_server2():
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())

    server_option, client_option, stat = option_stat()

    ret = pxblat.server.start_server_mt(
        "localhost", PORT, two_bit_file.as_posix(), server_option, stat
    )
    return ret


def test_server_status():
    server_option, client_option, stat = option_stat()
    extc.statusServer("localhost", str(PORT), server_option)


def test_query_server():
    extc.ServerOption().withCanStop(True).withStepSize(5).build()
    extc.queryServer(
        "query", "localhost", str(PORT), "tests/data/test_query.fa", False, False
    )


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
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} tests/data/ tests/data/test_case2.fa testc2.psl"
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
    option = extc.ServerOption().withCanStop(True).withStepSize(5).build()
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
        extc.ServerOption()
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
def pc(c):
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir("benchmark/data/")
        .withInName("benchmark/fas/chr20_2828159_2830288.fa")
        .build()
    )

    ret = extc.pygfClient(client_option)

    res = pxblat.read(ret, "psl")
    print(res)


@task
def test2(c):
    # open server
    server_option, client_option, stat = option_stat()
    start_server_mt_nb(
        "localhost", PORT, "tests/data/test_ref.2bit", server_option, stat
    )

    print("wait server ready")
    wait_server_ready("localhost", PORT)

    # .withInName("tests/data/test_case1.fa")
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir("tests/data/")
        .withInSeq(
            "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"
        )
        .build()
    )

    ret = pxblat.server.query_server(client_option)
    res = pxblat.read(ret, "psl")
    print(res)


def fas():
    for f in Path("./benchmark/fas/").glob("*.fa"):
        yield f


@task
def runp(c):
    server_option, _, stat = option_stat()
    two_bit = Path("tests/data/test_ref.2bit")
    # two_bit = Path("benchmark/data/chr20.2bit")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    print(server.status())
    print(server.files())

    # fa1 = list(fas())[0]
    fa1 = "tests/data/test_case1.fa"
    print(f"{fa1=}")

    # seq = "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(server.port))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .build()
    )

    client = ClientThread(client_option, server_option=server_option)
    client.start()

    ret = client.get()
    print(ret)


@task
def runp2(c):
    server_option, _, stat = option_stat()
    # two_bit = Path("tests/data/test_ref.2bit")
    two_bit = Path("benchmark/data/chr20.2bit")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    print(server.status())
    print(server.files())

    # fa1 = list(fas())[0]
    # fa1 = "tests/data/test_case1.fa"
    # fa1 = "benchmark/fas/chr20_2828159_2830288.fa"
    fa1 = "./t1.fa"

    print(f"{fa1=}")

    # seq = "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"
    # seq = "tgtaattccaactactcaggaggctgaggcaggagaatcgcttgagcccaggaggcggaggttgcagtgagccgagatcgcaccattgcactctagcctgggagacaagagcgaaactctgtctcaaaaaaaaaaaaagaaccaagttgaagga"
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(server.port))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .build()
    )

    parse = True
    client = ClientThread(client_option, server_option=server_option, parse=parse)
    client.start()

    ret = client.get()
    if not parse:
        with open("testt1p.psl", "w") as f:
            f.write(ret)
    else:
        print(f"python: {ret}")

    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1} testt1c.psl"
    )

    if parse:
        from Bio import SearchIO

        f = SearchIO.read("testt1.psl", "blat-psl")
        print(f"c {f}")


@task
def runcp(c):
    server_option, _, stat = option_stat()
    # two_bit = Path("tests/data/test_ref.2bit")
    two_bit = Path("benchmark/data/chr20.2bit")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    print(server.status())
    print(server.files())

    # fa1 = list(fas())[0]
    # fa1 = "tests/data/test_case1.fa"
    # fa1 = "benchmark/fas/chr20_2828159_2830288.fa"
    fa1 = "./t1.fa"

    print(f"{fa1=}")

    # seq = "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"
    # seq = "tgtaattccaactactcaggaggctgaggcaggagaatcgcttgagcccaggaggcggaggttgcagtgagccgagatcgcaccattgcactctagcctgggagacaagagcgaaactctgtctcaaaaaaaaaaaaagaaccaagttgaagga"
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(server.port))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .build()
    )
    parse = False

    client = ClientThread(client_option, server_option=server_option, parse=parse)
    client.start()

    if not parse:
        ret = client.get()
        with open("testt1p.psl", "w") as f:
            f.write(ret)
    else:
        print(f"python: {ret}")


@task
def runcs(c):
    c.run(
        f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog"
    )


@task
def read(c):
    from Bio import SearchIO

    f = SearchIO.read("testc2.psl", "blat-psl")
    print(f)


def compare_hsp(hsp1, hsp2):
    return (
        hsp1.query_start_all == hsp2.query_start_all
        and hsp1.query_end_all == hsp2.query_end_all
        and hsp1.hit_start_all == hsp2.hit_start_all
        and hsp1.hit_end_all == hsp2.hit_end_all
    )


def get_key_hsp(hsp):
    key = ""

    for i in sorted(hsp.query_start_all):
        key += str(i)

    for i in sorted(hsp.query_end_all):
        key += str(i)

    for i in sorted(hsp.hit_start_all):
        key += str(i)

    for i in sorted(hsp.hit_end_all):
        key += str(i)

    return key


def get_overlap(hsps1, hsps2):
    set1 = {get_key_hsp(i) for i in hsps1}
    set2 = {get_key_hsp(i) for i in hsps2}

    print(f"{len(set1)=} {len(set2)=}")

    overlap = set1 & set2

    print(f"overlap {len(overlap)=}")

    print(f"set1 - set2 {len(set1 - set2)=}")
    print(f"set2 - set1 {len(set2 - set1)=}")

    return set1 - set2, set2 - set1, set1 & set2


def _cpsl(file1, file2, isprint=True):
    # cc_psl = "./testt1cc.psl"
    # cp_psl = "./testt1cp2.psl"

    cc_psl = file1
    cp_psl = file2

    from Bio import SearchIO

    cc_res = SearchIO.read(cc_psl, "blat-psl")
    cp_res = SearchIO.read(cp_psl, "blat-psl")

    cc_hsps = cc_res.hsps
    cp_hsps = cp_res.hsps

    cc_hsps.sort(key=lambda x: x.score, reverse=True)
    cp_hsps.sort(key=lambda x: x.score, reverse=True)

    if isprint:
        for i in range(5):
            print(f"id {i} CC:")
            print(cc_hsps[i])
            print(f"id {i} CP:")
            print(cp_hsps[i])
            print(f"compare same:  {compare_hsp(cc_hsps[i], cp_hsps[i])}")
            print("\n")

    return get_overlap(cc_hsps, cp_hsps)


@task
def cpsl(c, file1: str, file2: str):
    _cpsl(file1, file2)


def cmd(cmd):
    print(f"worker {worker()}")
    # return subprocess.run(cmd, shell=True)
    return subprocess.check_output(cmd, shell=True)


@task
def bench(c, fa1: str):
    fa1_path = Path(fa1)

    cc_res = fa1_path.parent / f"{fa1_path.stem}_cc.psl"
    cp_res = fa1_path.parent / f"{fa1_path.stem}_cp.psl"

    two_bit = Path("benchmark/data/chr20.2bit")

    print("open c server")
    p = Process(
        target=cmd,
        args=(
            f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
        ),
    )
    p.start()

    time.sleep(8)

    print(f"run c client save to file {cc_res}")
    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1} {cc_res}"
    )

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .withOutName(cp_res.as_posix())
        .build()
    )
    parse = False
    client = ClientThread(client_option, parse=parse)
    client.start()
    client.get()

    print("stop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    p.terminate()

    time.sleep(3)

    ## python server

    pc_res = fa1_path.parent / f"{fa1_path.stem}_pc.psl"
    pp_res = fa1_path.parent / f"{fa1_path.stem}_pp.psl"

    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(1).build()
    )

    print("open python server")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    print(f"run python client save to file {pc_res}")
    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1} {pc_res}"
    )

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .withOutName(pp_res.as_posix())
        .build()
    )
    print(f"run python client save to file {pp_res}")
    parse = False
    client = ClientThread(client_option, parse=parse)
    client.start()

    client.get()


@task
def debug(c, fa1: str):
    fa1_path = Path(fa1)

    cc_res = fa1_path.parent / f"{fa1_path.stem}_cc.psl"
    cp_res = fa1_path.parent / f"{fa1_path.stem}_cp.psl"
    cp2_res = fa1_path.parent / f"{fa1_path.stem}_cp2.psl"

    two_bit = Path("benchmark/data/chr20.2bit")

    # print(f"open c server")

    # p = Process(
    #     target=cmd,
    #     args=(
    #         f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
    #     ),
    # )
    # p.start()

    # time.sleep(8)

    print(f"run c client save to file {cc_res}")
    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1} {cc_res}"
    )

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .withOutName(cp_res.as_posix())
        .build()
    )

    from pxblat.extc import pygfClient

    print(f"\n\n\nrun python client save to file {cp_res}")
    pygfClient(client_option)

    # parse = False
    # client = Client(client_option, parse=parse)
    # client.start()
    # ret = client.get()

    import pxblat._extc as ct

    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .withOutName(cp2_res.as_posix())
        .build()
    )

    print(f"\n\n\nrun python client save to file {cp2_res}")
    ct.cppbinding.pygfClient2(client_option)

    print("\n\n\nstop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    # p.terminate()


@task
def debugcc(c, fa1: str):
    fa1_path = Path(fa1)

    cc_res = fa1_path.parent / f"{fa1_path.stem}_cc.psl"

    two_bit = Path("benchmark/data/chr20.2bit")

    print(f"run c client save to file {cc_res}")
    c.run(
        f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1} {cc_res}"
    )


@task
def debugcp(c, fa1: str):
    fa1_path = Path(fa1)

    cp_res = fa1_path.parent / f"{fa1_path.stem}_cp.psl"

    two_bit = Path("benchmark/data/chr20.2bit")
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1)
        .withOutName(cp_res.as_posix())
        .build()
    )

    from pxblat.extc import pygfClient

    print(f"\n\n\nrun python client save to file {cp_res}")
    pygfClient(client_option)


@task
def benchsccp(c):
    two_bit = Path("benchmark/data/chr20.2bit")
    fas_path = Path("benchmark/test_fas")

    print("open c server")
    p = Process(
        target=cmd,
        args=(
            f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
        ),
    )
    p.start()
    time.sleep(8)

    for fa1_path in fas_path.glob("*.fa"):
        print(f"process {fa1_path}")
        cc_res = fa1_path.parent / f"{fa1_path.stem}_cc.psl"
        cp_res = fa1_path.parent / f"{fa1_path.stem}_cp.psl"

        print(f"run c client save to file {cc_res}")
        c.run(
            f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
        )

        client_option = (
            extc.ClientOption()
            .withMinScore(20)
            .withMinIdentity(90)
            .withHost("localhost")
            .withPort(str(PORT))
            .withSeqDir(two_bit.parent.as_posix())
            .withInName(fa1_path.as_posix())
            .withOutName(cp_res.as_posix())
            .build()
        )
        parse = False
        client = ClientThread(client_option, parse=parse)
        client.start()
        client.get()

    print("stop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    p.terminate()


@task
def benchspcp(c):
    two_bit = Path("benchmark/data/chr20.2bit")
    fas_path = Path("benchmark/test_fas")

    ## python server
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )

    print("open python server")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    for fa1_path in fas_path.glob("*.fa"):
        pc_res = fa1_path.parent / f"{fa1_path.stem}_pc.psl"
        pp_res = fa1_path.parent / f"{fa1_path.stem}_pp.psl"

        print(f"run python client save to file {pc_res}")
        c.run(
            f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path} {pc_res}"
        )

        client_option = (
            extc.ClientOption()
            .withMinScore(20)
            .withMinIdentity(90)
            .withHost("localhost")
            .withPort(str(PORT))
            .withSeqDir(two_bit.parent.as_posix())
            .withInName(fa1_path.as_posix())
            .withOutName(pp_res.as_posix())
            .build()
        )
        print(f"run python client save to file {pp_res}")
        parse = False
        client = ClientThread(client_option, parse=parse)
        client.start()
        client.get()

    server.stop()


@task
def cmpbench(c, fa_path: str):
    fas_path = Path(fa_path)

    num_files = 0

    for fa in fas_path.glob("*fa"):
        num_files += 1
        cc_res = fa.parent / f"{fa.stem}_cc.psl"
        pp_res = fa.parent / f"{fa.stem}_pp.psl"
        print(f"compare {cc_res} and {pp_res}")
        a, b, _ = _cpsl(cc_res, pp_res, False)
        assert len(a) == 0
        assert len(b) == 0

    print(f"compare {num_files} files")


@task
def cleanbench(c):
    fas_path = Path("benchmark/fas")
    for psl in fas_path.glob("*psl"):
        psl.unlink(missing_ok=True)


@task
def benchtimec(c, concurrent: int = 4, max_files: int = 4):
    fas_path = Path("benchmark/fas")
    Path("benchmark/data/chr20.2bit")

    print("open c server")
    p = Process(
        target=cmd,
        args=(
            f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
        ),
    )
    p.start()
    time.sleep(8)

    pool = ProcessPoolExecutor

    result = []
    start_time = time.perf_counter()
    with pool(concurrent) as executor:
        for idc, fa1_path in enumerate(fas_path.glob("*.fa")):
            if idc >= max_files:
                break

            # fa1_path.parent / f"{fa1_path.stem}_cc.psl"
            # run_cmd = f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            run_cmd = f"./bin/gfServer status localhost {PORT}"
            result.append(
                executor.submit(
                    cmd,
                    run_cmd,
                )
            )
            print(f"submit {fa1_path}")

        for ret in result:
            ret.result()
            # c.run(
            #     f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            # )

    dura_c = time.perf_counter() - start_time
    print(f"run c tool in {concurrent} parallel, time: {dura_c:.4}s")

    print("stop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    p.terminate()

    time.sleep(3)


@task
def benchtimep(c, concurrent: int = 4, max_files: int = 4):
    fas_path = Path("benchmark/fas")
    two_bit = Path("benchmark/data/chr20.2bit")

    ## python server
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )

    print("open python server")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    pool = ProcessPoolExecutor
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(1).build()
    )
    result = []
    start_time = time.perf_counter()

    from pxblat.extc import pystatusServer

    with pool(concurrent) as executor:
        for idp, fa1_path in enumerate(fas_path.glob("*.fa")):
            # fa1_path.parent / f"{fa1_path.stem}_pp.psl"
            if idp >= max_files:
                break
            # client_option = (
            #     extc.ClientOption()
            #     .withMinScore(20)
            #     .withMinIdentity(90)
            #     .withHost("localhost")
            #     .withPort(str(PORT))
            #     .withSeqDir(two_bit.parent.as_posix())
            #     .withInName(fa1_path.as_posix())
            #     .withOutName(pp_res.as_posix())
            #     .build()
            # )
            # result.append(executor.submit(query_server, client_option))
            result.append(
                # executor.submit(status_server, "localhost", PORT, server_option)
                executor.submit(pystatusServer, "localhost", str(PORT), server_option)
            )
            print(f"submit {fa1_path}")

        # for ret in result:
        # ret.done()

    dura_py = time.perf_counter() - start_time
    print(f"run python in {concurrent} parallel, time: {dura_py:.4}s")

    server.stop()


def status_server_c():
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )
    return extc.pystatusServer("localhost", str(PORT), server_option)


@task
def benchtimepcp(c, concurrent: int = 4, max_files: int = 4):
    fas_path = Path("benchmark/fas")
    two_bit = Path("benchmark/data/chr20.2bit")

    ## python server
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )

    print("open python server")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    pool = ThreadPoolExecutor

    result = []
    start_time = time.perf_counter()

    with pool(concurrent) as executor:
        for idp, fa1_path in enumerate(fas_path.glob("*.fa")):
            # fa1_path.parent / f"{fa1_path.stem}_pp.psl"
            if idp >= max_files:
                break

            # client_option = (
            #     extc.ClientOption()
            #     .withMinScore(20)
            #     .withMinIdentity(90)
            #     .withHost("localhost")
            #     .withPort(str(PORT))
            #     .withSeqDir(two_bit.parent.as_posix())
            #     .withInName(fa1_path.as_posix())
            #     .withOutName(pp_res.as_posix())
            #     .build()
            # )
            # result.append(executor.submit(query_server, client_option))
            result.append(
                executor.submit(status_server, "localhost", PORT, server_option)
                # executor.submit(status_server_c)
            )
            print(f"submit {fa1_path}")
            dummy_work(10)

        for ret in result:
            ret.result()

    dura_py = time.perf_counter() - start_time
    print(f"run python in {concurrent} parallel, time: {dura_py:.4}s")

    time.sleep(1)

    pool = ThreadPoolExecutor

    result = []
    start_time = time.perf_counter()
    with pool(concurrent) as executor:
        for idc, fa1_path in enumerate(fas_path.glob("*.fa")):
            if idc >= max_files:
                break

            # fa1_path.parent / f"{fa1_path.stem}_cc.psl"
            # run_cmd = f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            run_cmd = f"./bin/gfServer status localhost {PORT}"
            result.append(
                executor.submit(
                    cmd,
                    run_cmd,
                )
            )
            print(f"submit {fa1_path}")
            dummy_work(10)

        for ret in result:
            ret.result()
            # c.run(
            #     f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            # )

    dura_c = time.perf_counter() - start_time
    print(f"run c tool in {concurrent} parallel, time: {dura_c:.4}s")

    server.stop()


@task
def benchtimeccp(c, concurrent: int = 4, max_files: int = 4):
    fas_path = Path("benchmark/fas")
    Path("benchmark/data/chr20.2bit")

    print("open c server")
    p = Process(
        target=cmd,
        args=(
            f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
        ),
    )
    p.start()
    time.sleep(8)

    pool = ProcessPoolExecutor
    result = []
    start_time = time.perf_counter()

    with pool(concurrent) as executor:
        for idp, fa1_path in enumerate(fas_path.glob("*.fa")):
            # fa1_path.parent / f"{fa1_path.stem}_pp.psl"
            if idp >= max_files:
                break

            # client_option = (
            #     extc.ClientOption()
            #     .withMinScore(20)
            #     .withMinIdentity(90)
            #     .withHost("localhost")
            #     .withPort(str(PORT))
            #     .withSeqDir(two_bit.parent.as_posix())
            #     .withInName(fa1_path.as_posix())
            #     .withOutName(pp_res.as_posix())
            #     .build()
            # )
            # result.append(executor.submit(query_server, client_option))
            result.append(
                # executor.submit(status_server, "localhost", PORT, server_option)
                executor.submit(status_server_c)
            )
            print(f"submit {fa1_path}")
            dummy_work(10)

        for ret in result:
            ret.result()

    dura_py = time.perf_counter() - start_time
    print(f"run python in {concurrent} parallel, time: {dura_py:.4}s")

    time.sleep(1)

    pool = ProcessPoolExecutor

    result = []
    start_time = time.perf_counter()
    with pool(concurrent) as executor:
        for idc, fa1_path in enumerate(fas_path.glob("*.fa")):
            if idc >= max_files:
                break

            # fa1_path.parent / f"{fa1_path.stem}_cc.psl"
            # run_cmd = f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            run_cmd = f"./bin/gfServer status localhost {PORT}"
            result.append(
                executor.submit(
                    cmd,
                    run_cmd,
                )
            )
            print(f"submit {fa1_path}")
            dummy_work(10)

        for ret in result:
            ret.result()
            # c.run(
            #     f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            # )

    dura_c = time.perf_counter() - start_time
    print(f"run c tool in {concurrent} parallel, time: {dura_c:.4}s")

    print("stop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    p.terminate()


@task
def benchscc(c, fa_path: str, concurrent: int = 4):
    two_bit = Path("benchmark/data/chr20.2bit")
    fas_path = Path(fa_path)

    print("open c server")
    p = Process(
        target=cmd,
        args=(
            f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog",
        ),
    )
    p.start()
    time.sleep(8)

    pool = ThreadPoolExecutor

    result = []
    start_time = time.perf_counter()
    with pool(concurrent) as executor:
        for fa1_path in fas_path.glob("*.fa"):
            print(f"process {fa1_path}")
            cc_res = fa1_path.parent / f"{fa1_path.stem}_cc.psl"

            # c.run(
            #     f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"
            # )
            run_cmd = f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} {two_bit.parent.as_posix()} {fa1_path.as_posix()} {cc_res}"

            result.append(
                executor.submit(
                    cmd,
                    run_cmd,
                )
            )

        for ret in result:
            ret.result()

    dura_c = time.perf_counter() - start_time
    print(f"run c gfserver and gfclient time: {dura_c:.4}s")

    print("stop c server")
    c.run(f"./bin/gfServer stop localhost {PORT}")
    p.terminate()


def query_server2(two_bit, fa1_path, pp_res):
    client_option = (
        extc.ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir(two_bit.parent.as_posix())
        .withInName(fa1_path.as_posix())
        .withOutName(pp_res.as_posix())
        .build()
    )

    ret = pygfClient(client_option)
    # ret = pygfClient_no_gil(client_option)
    # ret = query_server(client_option, parse=False)
    print(f"worker {worker()} ")
    return ret


@task
def benchspp(c, fa_path: str, concurrent: int = 4):
    two_bit = Path("benchmark/data/chr20.2bit")
    fas_path = Path(fa_path)

    ## python server
    server_option = extc.ServerOption().withCanStop(True).withStepSize(5).build()
    print("open python server")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    pool = ThreadPoolExecutor
    # pool = ProcessPoolExecutor

    result = []
    start_time = time.perf_counter()
    with pool(concurrent) as executor:
        for fa1_path in fas_path.glob("*.fa"):
            pp_res = fa1_path.parent / f"{fa1_path.stem}_pp.psl"

            (
                extc.ClientOption()
                .withMinScore(20)
                .withMinIdentity(90)
                .withHost("localhost")
                .withPort(str(PORT))
                .withSeqDir(two_bit.parent.as_posix())
                .withInName(fa1_path.as_posix())
                .withOutName(pp_res.as_posix())
                .build()
            )

            executor.submit(
                query_server2,
                two_bit,
                fa1_path,
                pp_res,
            )

            # executor.submit(pygfClient_no_gil, client_option)
            print(f"run python client save to file {pp_res}")

        for res in result:
            res.result()

    dura_py = time.perf_counter() - start_time
    print(f"run python server and client time: {dura_py:.4}s")
    server.stop()


changes = [
    "src/hg/altSplice/altSplice/genePredToPsl.c",
    "src/hg/cgilib/cartJson.c",
    "src/hg/cgilib/pcrResult.c",
    "src/hg/hgGene/domains.c",
    "src/hg/hgHubConnect/hgHubConnect.c",
    "src/hg/hgPhyloPlace/hgPhyloPlace.c",
    "src/hg/hgPhyloPlace/phyloPlace.c",
    "src/hg/hgPhyloPlace/phyloPlaceMain.c",
    "src/hg/hgPhyloPlace/treeToAuspiceJson.c",
    "src/hg/hgPhyloPlace/vcfFromFasta.c",
    "src/hg/hgSearch/hgSearch.c",
    "src/hg/hgSession/hgSession.c",
    "src/hg/hgTables/mainPage.c",
    "src/hg/hgTracks/bigWigTrack.c",
    "src/hg/hgTracks/hgTracks.c",
    "src/hg/hgTracks/simpleTracks.c",
    "src/hg/hgTracks/wigCommon.h",
    "src/hg/hgTracks/wigTrack.c",
    "src/hg/hgc/hgc.c",
    "src/hg/hubApi/list.c",
    "src/hg/inc/botDelay.h",
    "src/hg/inc/cartJson.h",
    "src/hg/inc/hgMaf.h",
    "src/hg/inc/versionInfo.h",
    "src/hg/lib/bigBedFind.c",
    "src/hg/lib/botDelay.c",
    "src/hg/lib/cart.c",
    "src/hg/lib/dupTrack.c",
    "src/hg/lib/hgMaf.c",
    "src/hg/lib/hubConnect.c",
    "src/hg/lib/trackHub.c",
    "src/hg/lib/web.c",
    "src/hg/mouseStuff/axtChain/axtChain.c",
    "src/inc/net.h",
    "src/inc/srcVersion.h",
    "src/lib/https.c",
    "src/lib/net.c",
    "src/lib/pslTransMap.c",
    "src/lib/udc.c",
    "src/hg/altSplice/altSplice/genePredToPsl.c",
    "src/hg/cgilib/cartJson.c",
    "src/hg/cgilib/pcrResult.c",
    "src/hg/hgGene/domains.c",
    "src/hg/hgHubConnect/hgHubConnect.c",
    "src/hg/hgPhyloPlace/hgPhyloPlace.c",
    "src/hg/hgPhyloPlace/phyloPlace.c",
    "src/hg/hgPhyloPlace/phyloPlaceMain.c",
    "src/hg/hgPhyloPlace/treeToAuspiceJson.c",
    "src/hg/hgPhyloPlace/vcfFromFasta.c",
    "src/hg/hgSearch/hgSearch.c",
    "src/hg/hgSession/hgSession.c",
    "src/hg/hgTables/mainPage.c",
    "src/hg/hgTracks/bigWigTrack.c",
    "src/hg/hgTracks/hgTracks.c",
    "src/hg/hgTracks/simpleTracks.c",
    "src/hg/hgTracks/wigCommon.h",
    "src/hg/hgTracks/wigTrack.c",
    "src/hg/hgc/hgc.c",
    "src/hg/hubApi/list.c",
    "src/hg/inc/botDelay.h",
    "src/hg/inc/cartJson.h",
    "src/hg/inc/hgMaf.h",
    "src/hg/inc/versionInfo.h",
    "src/hg/lib/bigBedFind.c",
    "src/hg/lib/botDelay.c",
    "src/hg/lib/cart.c",
    "src/hg/lib/dupTrack.c",
    "src/hg/lib/hgMaf.c",
    "src/hg/lib/hubConnect.c",
    "src/hg/lib/trackHub.c",
    "src/hg/lib/web.c",
    "src/hg/mouseStuff/axtChain/axtChain.c",
    "src/inc/net.h",
    "src/inc/srcVersion.h",
    "src/lib/https.c",
    "src/lib/net.c",
    "src/lib/pslTransMap.c",
    "src/lib/udc.c",
]


@task
def search_source(c):
    sources = list(get_files_by_suffix("src/pxblat/extc/src", [".c"]))
    headers = list(get_files_by_suffix("src/pxblat/extc/include", [".h"]))
    sources.extend(headers)

    print(sources)

    change_files = [Path(file) for file in changes]

    for file in change_files:
        for source in sources:
            if source.name == file.name:
                print(f"{file} is in sources {source}")
                break


@task
def tpickle(c):
    import pickle

    c = pxblat.ClientOption()
    c.withHost("localhost2").build()
    cdata = pickle.dumps(c)
    cn = pickle.loads(cdata)
    print(cn)
