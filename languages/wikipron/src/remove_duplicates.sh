#!/bin/bash
set -eou pipefail

for TSV in ../tsv/*.tsv; do
    sort -u -o "${TSV}" "${TSV}"
done