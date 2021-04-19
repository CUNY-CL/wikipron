# Error analysis tool for grapheme-to-phoneme (g2p) conversion

This tool performs a fine-grained error analysis of a G2P model. It prints a
"performance matrix" comparing the gold and hypothesized results of a G2P model.

The performance matrix is a 2x2 table where the dimensions are:

-   whether the hypothesized pronunciation matches the corpus prediction and
-   whether the hypothesized pronunciation adheres to the spelling rules of the
    language and script, according to a user-provided covering grammar.

## Prerequisites

The script requires [PrettyTable](https://pypi.org/project/prettytable/) and
[Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini).

```bash
conda install -c conda-forge pynini
pip install prettytable
```

### Data

Two input files are required:

1.  Covering grammar: a two-column TSV file in which the left column contains
    zero or more graphemes, and the right contains zero or more phones it can
    correspond to.
2.  Test output: a three-column TSV file in which the columns are the graphemic
    form, the gold pronunciation, and the hypothesized pronunciation.

## Example workflow

```bash
cd data/src/error_analysis
./error_analysis.py --cg_path=cg.tsv --test_path=test.tsv
```
