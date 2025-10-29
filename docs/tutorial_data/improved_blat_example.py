"""Improved BLAT alignment function with better resource management.

This example shows how to use the pxblat Client and Server with proper
resource handling to avoid the query limit issue.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from Bio.Seq import Seq

from pxblat import Client, Server
from pxblat.toolkit import fa_to_two_bit

if TYPE_CHECKING:
    from collections.abc import Sequence


def blat(
    seqs: Sequence[tuple[Seq | str, Seq | str]],
    ref: Path,
    host: str = "localhost",
    port: int = 65000,
) -> list:
    """Align sequences to a reference genome.

    Args:
        seqs: Sequence of (name, sequence) tuples to align
        ref: Path to reference genome FASTA file
        host: Server hostname (default: localhost)
        port: Server port (default: 65000)

    Returns:
        List of QueryResult objects from BLAT alignment
    """
    two_bit = ref.with_suffix(".2bit")

    # Convert FASTA to 2bit format if needed
    if not two_bit.exists():
        fa_to_two_bit(
            [ref.as_posix()],
            two_bit.as_posix(),
            noMask=False,
            stripVersion=False,
            ignoreDups=False,
            useLong=False,
        )

    # Use server as context manager for proper cleanup
    server = Server(host, port, two_bit.as_posix())

    results = []
    with server:
        server.wait_ready()

        # Create client after server is ready
        client = Client(
            host,
            port,
            seq_dir=ref.parent.as_posix(),
            min_score=10,
        )

        # Process sequences
        for i, seq in enumerate(seqs, 1):
            seq_str = str(seq[1]) if isinstance(seq[1], Seq) else seq[1]
            result = client.query(seq_str)
            results.append(result)

            if i % 100 == 0:
                print(f"Processed {i}/{len(seqs)} sequences")

    return results


def blat_batched(
    seqs: Sequence[tuple[Seq | str, Seq | str]],
    ref: Path,
    host: str = "localhost",
    port: int = 65000,
    batch_size: int = 500,
) -> list:
    """Align sequences to a reference genome with batching.

    This version processes sequences in batches and can be more memory-efficient
    for very large datasets.

    Args:
        seqs: Sequence of (name, sequence) tuples to align
        ref: Path to reference genome FASTA file
        host: Server hostname (default: localhost)
        port: Server port (default: 65000)
        batch_size: Number of sequences to process in each batch

    Returns:
        List of QueryResult objects from BLAT alignment
    """
    two_bit = ref.with_suffix(".2bit")

    # Convert FASTA to 2bit format if needed
    if not two_bit.exists():
        fa_to_two_bit(
            [ref.as_posix()],
            two_bit.as_posix(),
            noMask=False,
            stripVersion=False,
            ignoreDups=False,
            useLong=False,
        )

    # Use server as context manager for proper cleanup
    server = Server(host, port, two_bit.as_posix())

    results = []
    with server:
        server.wait_ready()

        # Create client after server is ready
        client = Client(
            host,
            port,
            seq_dir=ref.parent.as_posix(),
            min_score=10,
        )

        # Process in batches
        total = len(seqs)
        for start_idx in range(0, total, batch_size):
            end_idx = min(start_idx + batch_size, total)
            batch = seqs[start_idx:end_idx]

            print(f"Processing batch {start_idx // batch_size + 1} ({start_idx + 1}-{end_idx}/{total})")

            for seq in batch:
                seq_str = str(seq[1]) if isinstance(seq[1], Seq) else seq[1]
                result = client.query(seq_str)
                results.append(result)

    return results


# Example usage
if __name__ == "__main__":
    # Example sequences (name, sequence)
    example_seqs = [
        ("seq1", "ATCGATCGATCG"),
        ("seq2", "GCTAGCTAGCTA"),
        # Add more sequences here
    ]

    ref_path = Path("reference.fa")

    # Use the improved function
    results = blat(example_seqs, ref_path)
    print(f"Processed {len(results)} sequences successfully!")
