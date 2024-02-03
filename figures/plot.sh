#!/bin/bash
set -e
set -u
set -o pipefail

python fas_len.py
python bench.py
