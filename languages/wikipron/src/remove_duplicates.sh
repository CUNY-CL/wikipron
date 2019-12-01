#!/bin/bash
set -eou pipefail

for TSV in ../tsv/*.tsv; do
    # Explicitly uses byte-wise comparison for sorting
    # rather than a locale-dependent comparison.
    LC_ALL=C sort -u -o "${TSV}" "${TSV}"
done