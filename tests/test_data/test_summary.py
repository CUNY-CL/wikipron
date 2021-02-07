import os

_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
_SUMMARY = os.path.join(_REPO_DIR, "data/tsv_summary.tsv")
_TSV_DIRECTORY = os.path.join(_REPO_DIR, "data/tsv")


def test_summary_matches_language_data():
    """Check if each TSV referenced in data/tsv_summary.tsv is
    present in data/tsv.

    (Basically checks whether generate_tsv_summary.py has been run.)
    """
    observed_name_to_count = {}

    for unique_tsv in os.listdir(_TSV_DIRECTORY):
        with open(
            f"{_TSV_DIRECTORY}/{unique_tsv}", "r", encoding="utf-8"
        ) as tsv:
            num_of_entries = sum(1 for line in tsv)
            observed_name_to_count[unique_tsv] = num_of_entries

    with open(_SUMMARY, "r", encoding="utf-8") as lang_summary:
        summary_files = [line.rstrip().split("\t")[0] for line in lang_summary]

    for summary_file in summary_files:
        assert (
            summary_file in observed_name_to_count
        ), f"{summary_file} in data/tsv_summary.tsv but not in data/tsv"


def test_language_data_matches_summary():
    """Check if each TSV in data/tsv is present in data/tsv_summary.tsv
    and if the number of entries in each TSV matches its listed number
    of entries in data/tsv_summary.tsv.

    (Basically checks whether generate_tsv_summary.py has been run.)
    """
    name_count_dict = {}
    with open(_SUMMARY, "r", encoding="utf-8") as lang_summary:
        vals = [line.rstrip().split("\t") for line in lang_summary]
        for val in vals:
            name_count_dict[val[0]] = int(val[-1])

    for unique_tsv in os.listdir(_TSV_DIRECTORY):
        with open(
            f"{_TSV_DIRECTORY}/{unique_tsv}", "r", encoding="utf-8"
        ) as tsv:
            num_of_entries = sum(1 for line in tsv)
        assert unique_tsv in name_count_dict, (
            f"{unique_tsv} in data/tsv but not in " "data/tsv_summary.tsv"
        )
        assert name_count_dict[unique_tsv] == num_of_entries, (
            f"Number of entries in {unique_tsv} does not match "
            "number of entries in data/tsv_summary.tsv."
        )
