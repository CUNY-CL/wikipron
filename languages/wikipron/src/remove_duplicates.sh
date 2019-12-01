#!/bin/bash
set -eou pipefail

for TSV in ../tsv/*.tsv; do
    LC_ALL=C sort -u -o "${TSV}" "${TSV}"
done