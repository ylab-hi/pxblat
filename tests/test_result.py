from __future__ import annotations
import subprocess
import sys
import time
from multiprocessing import Process
from pathlib import Path

import pxblat
import pytest
from pxblat import Client
from rich import print

from Bio import SearchIO


@pytest.fixture()
def fas():
    return Path("tests/data/fas")


def is_linux():
    return sys.platform.startswith("linux")


def is_mac():
    return sys.platform.startswith("darwin")


def find_base_path():
    base_path = Path("./tests") / "blat"

    if is_linux():
        blat_path = base_path / "linux"
    elif is_mac():
        blat_path = base_path / "darwin"
    else:
        raise RuntimeError("Unsupported platform.")

    return blat_path


def find_gfserver():
    path = find_base_path() / "gfServer"
    path.chmod(0o755)
    return path


def find_gfclient():
    path = find_base_path() / "gfClient"
    path.chmod(0o755)
    return path


def run_cmd(cmd):
    subprocess.run(cmd, shell=True)


def run_cblat(result_dir: Path, port: int, fa_data: Path):
    cport = port + 20
    two_bit = Path("benchmark/data/chr20.2bit")

    gfserver = find_gfserver()
    gfclient = find_gfclient()

    print("open c server")

    p = Process(
        target=run_cmd,
        args=(f"{gfserver} start localhost {cport} {two_bit} -canStop -stepSize=5",),
    )
    p.start()
    time.sleep(5)

    fa_files = [fa_data] if fa_data.suffix == ".fa" else fa_data.glob("*.fa")

    for _, fa in enumerate(fa_files):
        print(f"run cc {fa}")
        cc_res = result_dir / f"{fa.stem}_cc.psl"
        run_cmd(
            f"{gfclient} -minScore=20 -minIdentity=90 localhost {cport} {two_bit.parent.as_posix()} {fa} {cc_res}"
        )

    print("stop c server")
    run_cmd(f"{gfserver} stop localhost {cport}")


def run_pxblat_async(result_dir: Path, port: int, fa_data: Path):
    cport = port + 20
    two_bit = Path("benchmark/data/chr20.2bit")
    server_option = pxblat.ServerOption().withCanStop(True).withStepSize(5).build()

    print("open python server")
    server = pxblat.Server("localhost", cport, two_bit, server_option)
    server.start()
    server.wait_ready()
    results = {}

    client = Client(
        host="localhost",
        port=cport,
        seq_dir=two_bit.parent.as_posix(),
        min_score=20,
        min_identity=90,
    )

    fa_files = (
        [fa_data] if fa_data.suffix == ".fa" else [fa for fa in fa_data.glob("*.fa")]
    )
    # fa_files = [Path("tests/data/fas/chr20_434138_436331.fa")]

    ret = client.query(fa_files)

    for r, fa in zip(ret, fa_files):
        print(f"run px {fa}")
        results[fa.stem] = r

    server.stop()
    return results


def run_pxblat(result_dir: Path, port: int, fa_data: Path):
    cport = port + 20
    two_bit = Path("benchmark/data/chr20.2bit")
    server_option = pxblat.ServerOption().withCanStop(True).withStepSize(5).build()

    print("open python server")
    server = pxblat.Server("localhost", cport, two_bit, server_option)
    server.start()
    server.wait_ready()
    results = {}

    fa_files = [fa_data] if fa_data.suffix == ".fa" else fa_data.glob("*.fa")
    for _, fa in enumerate(fa_files):
        client_option = (
            pxblat.ClientOption()
            .withMinScore(20)
            .withMinIdentity(90)
            .withHost("localhost")
            .withPort(str(cport))
            .withSeqDir(two_bit.parent.as_posix())
            .withInName(fa.as_posix())
            .build()
        )

        client = pxblat.ClientThread(client_option)
        client.start()
        ret = client.get()
        results[fa.stem] = ret

    server.stop()
    return results


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


def compare_hsp(hsp1, hsp2):
    return (
        hsp1.query_start_all == hsp2.query_start_all
        and hsp1.query_end_all == hsp2.query_end_all
        and hsp1.hit_start_all == hsp2.hit_start_all
        and hsp1.hit_end_all == hsp2.hit_end_all
    )


def get_overlap(hsps1, hsps2):
    set1 = {get_key_hsp(i) for i in hsps1}
    set2 = {get_key_hsp(i) for i in hsps2}
    return set1 - set2, set2 - set1, set1 & set2


def _cpsl(file1, file2, isprint=False):
    cc_psl = file1
    cp_psl = file2

    cc_res = None
    try:
        cc_res = SearchIO.read(cc_psl, "blat-psl")
    except ValueError as e:
        if "No query results" in str(e):
            print("no result found")
            cc_res = None

    if isinstance(cp_psl, (Path, str)):
        cp_res = SearchIO.read(cp_psl, "blat-psl")
    else:
        cp_res = cp_psl

    if cc_res is None and cp_res is None:
        return

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


def create_result(result_dir, port, fa_data):
    run_cblat(result_dir, port, fa_data)
    results = run_pxblat_async(result_dir, port, fa_data)
    return results


def time_creat_result(result_dir, port, fas):
    cstart = time.perf_counter()
    run_cblat(result_dir, port, fas)
    cend = time.perf_counter()
    print(f"run_cblat time: {cend - cstart:.4f}")

    pstart = time.perf_counter()
    results = run_pxblat_async(result_dir, port, fas)
    pend = time.perf_counter()
    print(f"run_pxblat time: {pend - pstart:.4f}")

    speedup = (cend - cstart) / (pend - pstart)
    print(f"speed up: {speedup:.4f}x")

    return results


def test_result_c_with_py(tmpdir, port, fas, *, time=True, compare=True):
    pxblat_results = (
        create_result(tmpdir, port, fas)
        if not time
        else time_creat_result(tmpdir, port, fas)
    )

    if compare:
        file_num = 0
        for fa in fas.glob("*fa"):
            file_num += 1
            cc_res = tmpdir / f"{fa.stem}_cc.psl"
            pp_res = pxblat_results[fa.stem]

            _ret = _cpsl(cc_res, pp_res)
            if _ret is None:
                return
            a, b, _ = _ret
            assert len(a) == 0
            assert len(b) == 0
        print(f"test {file_num} files")


@pytest.mark.failing
@pytest.mark.parametrize(
    "failing_fas",
    [
        Path("tests/data/fas/chr20_11648866_11650925.fa"),
        Path("benchmark/fas/chr20_30806959_30809757.fa"),
    ],
)
def test_failing_case(tmpdir, port, failing_fas, time=False):
    pxblat_results = (
        create_result(tmpdir, port, failing_fas)
        if not time
        else time_creat_result(tmpdir, port, failing_fas)
    )

    file_num = 0
    for fa in [failing_fas]:
        file_num += 1
        cc_res = tmpdir / f"{fa.stem}_cc.psl"
        pp_res = pxblat_results[fa.stem]

        _ret = _cpsl(cc_res, pp_res)
        if _ret is None:
            return
        a, b, _ = _ret
        assert len(a) == 0
        assert len(b) == 0

    print(f"test {file_num} files")


if __name__ == "__main__":
    from pathlib import Path

    tmpdir = Path("tmp")
    tmpdir.mkdir(exist_ok=True)
    port = 65000
    fa = Path("tests/data/fas/")
    fa1 = Path("benchmark/fas/1")
    fa2 = Path("benchmark/fas/2")
    fa3 = Path("benchmark/fas/3")
    fa4 = Path("benchmark/fas/4")
    fa5 = Path("benchmark/fas/5")
    fa6 = Path("benchmark/fas/6")
    # test_fas = Path("benchmark/test_fas")

    test_result_c_with_py(tmpdir, port, fa, time=False, compare=True)
    # time.sleep(5)
    # test_result_c_with_py(tmpdir, port, fa1, time=False, compare=True)
