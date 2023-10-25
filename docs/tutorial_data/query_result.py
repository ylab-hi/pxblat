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
    return [result1, result2, result3, result4, result5, result6]


def query_result():
    results = query_context()  # get all alignment results
    results[2]  # let's pick up the result of test_case1.fa
    result3 = results[2]
    print(result3)
    print(result3[0])  # let's show information of the result
    result = result3[0]  # let's get the element in the result list
    print(result)
    print(result)
    print(result.hsps)  # check all  high-scoring pairs (HSPs)
    print(result[0])  # check the top hsp
    print(result[0])  # show more information about top hsp
    top_hsp = result.hsps[0]
    print(top_hsp)
    print(top_hsp)
    print(top_hsp.query_id)  # test_case1's id in top_hsp
    print(top_hsp.query_range)  # test_case1's query_range in top_hsp
    print(top_hsp.query_span)  # test_case1's query_span in top_hsp
    print(top_hsp.query_start)  # test_case1's query_start in top_hsp
    print(top_hsp.query_strand)  # test_case1's query_strand in top_hsp
    print(top_hsp.hit_id)  # in top_hsp, test_case1 hit `chr1` of the reference
    print(top_hsp.hit_range)  #  in top_hsp, test_case1 hit (12699, 12850) of the reference
    print(top_hsp.hit_start)
    print(top_hsp.hit_strand)  # in top_hsp, test_case1 hit strand of the reference (1 means positive strand)
    # >>> top_hsp.
    # top_hsp.aln                 top_hsp.hit_frame           top_hsp.ident_pct           top_hsp.query_frame_all
    # top_hsp.aln_all             top_hsp.hit_frame_all       top_hsp.is_fragmented       top_hsp.query_gap_num
    # top_hsp.aln_annotation      top_hsp.hit_gap_num         top_hsp.match_num           top_hsp.query_gapopen_num
    # top_hsp.aln_annotation_all  top_hsp.hit_gapopen_num     top_hsp.match_rep_num       top_hsp.query_id
    # top_hsp.aln_span            top_hsp.hit_id              top_hsp.mismatch_num        top_hsp.query_inter_ranges
    # top_hsp.fragment            top_hsp.hit_inter_ranges    top_hsp.molecule_type       top_hsp.query_inter_spans
    # top_hsp.fragments           top_hsp.hit_inter_spans     top_hsp.n_num               top_hsp.query_is_protein
    # top_hsp.gap_num             top_hsp.hit_range           top_hsp.output_index        top_hsp.query_range
    # top_hsp.gapopen_num         top_hsp.hit_range_all       top_hsp.query               top_hsp.query_range_all
    # top_hsp.hit                 top_hsp.hit_span            top_hsp.query_all           top_hsp.query_span
    # top_hsp.hit_all             top_hsp.hit_span_all        top_hsp.query_description   top_hsp.query_span_all
    # top_hsp.hit_description     top_hsp.hit_start           top_hsp.query_end           top_hsp.query_start
    # top_hsp.hit_end             top_hsp.hit_start_all       top_hsp.query_end_all       top_hsp.query_start_all
    # top_hsp.hit_end_all         top_hsp.hit_strand          top_hsp.query_features      top_hsp.query_strand
    # top_hsp.hit_features        top_hsp.hit_strand_all      top_hsp.query_features_all  top_hsp.query_strand_all
    # top_hsp.hit_features_all    top_hsp.ident_num           top_hsp.query_frame         top_hsp.score


if __name__ == "__main__":
    query_result()
