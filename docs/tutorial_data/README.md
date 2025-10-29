# PxBLAT Tutorial Examples

This directory contains example code for the PxBLAT tutorial.

## Files

### Basic Examples

- **`2bit.py`** - Working with 2bit format files
- **`blat.py`** - Basic BLAT alignment usage
- **`query_context.py`** - Query context examples
- **`query_general.py`** - General query operations
- **`query_result.py`** - Handling and parsing results

### Advanced Examples

- **`improved_blat_example.py`** - Production-ready BLAT alignment with:
  - Proper resource management
  - Batch processing support
  - Progress tracking
  - Automatic 2bit conversion
  - Large-scale sequence processing (1000+ sequences)

## Usage

### Basic Example

```python
from pxblat import Client, Server

# See blat.py for basic usage
```

### Large-Scale Processing

```python
from pathlib import Path

# Copy the blat() or blat_batched() function from improved_blat_example.py
sequences = [("seq1", "ATCG..."), ("seq2", "GCTA..."), ...]
results = blat(sequences, Path("reference.fa"))
```

## Reference Data

- **`test_case1.fa`** - Sample query sequences
- **`test_ref.fa`** - Sample reference genome
- **`test_ref.2bit`** - Pre-converted 2bit reference

## Documentation

All examples are referenced in the main tutorial:
https://pxblat.readthedocs.io/en/latest/tutorial.html

## Downloading Examples

```bash
# Download a specific example
wget https://raw.githubusercontent.com/ylab-hi/pxblat/main/docs/tutorial_data/improved_blat_example.py

# Or clone the entire repository
git clone https://github.com/ylab-hi/pxblat.git
cd pxblat/docs/tutorial_data
```
