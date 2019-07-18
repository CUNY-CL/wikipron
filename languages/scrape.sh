#!/bin/bash

set -eou pipefail

g2p fra \
    --no-syllable-boundaries \
    --dialect European \
    --casefold \
    --cut-off-date 2019-07-15 \
    --output fra_lexicon_raw.tsv
