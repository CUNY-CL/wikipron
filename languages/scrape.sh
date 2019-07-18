#!/bin/bash

set -eou pipefail

g2p French \
    --no-syllable-boundaries \
    --dialect European \
    --casefold \
    --cut-off-date 2019-7-15 \
    --output fra_lexicon_raw.tsv
