import os

_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
_TSV_SUMMARY = os.path.join(_REPO_DIR, "data/scrape/tsv_summary.tsv")
_TSV_DIRECTORY = os.path.join(_REPO_DIR, "data/scrape/tsv")
_PHONES_SUMMARY = os.path.join(_REPO_DIR, "data/phones/phones_summary.tsv")
_PHONES_DIRECTORY = os.path.join(_REPO_DIR, "data/phones/phones")


def test_language_data_matches_summary():
    """Check if each TSV in data/tsv is present in data/tsv_summary.tsv
    (and vice-versa) as well as if the number of entries in each TSV in
    data/tsv matches its listed number of entries in data/tsv_summary.tsv.

    (Basically checks whether generate_tsv_summary.py has been run.)
    """
    name_to_count = {}
    with open(_TSV_SUMMARY, "r", encoding="utf-8") as lang_summary:
        for line in lang_summary:
            language = line.rstrip().split("\t")
            name_to_count[language[0]] = int(language[-1])

    for unique_tsv in os.listdir(_TSV_DIRECTORY):
        with open(
            f"{_TSV_DIRECTORY}/{unique_tsv}", "r", encoding="utf-8"
        ) as tsv:
            num_of_entries = sum(1 for line in tsv)
        assert unique_tsv in name_to_count, (
            f"{unique_tsv} in data/tsv but not in " "data/tsv_summary.tsv"
        )
        assert name_to_count[unique_tsv] == num_of_entries, (
            f"Number of entries in {unique_tsv} does not match "
            "number of entries in data/tsv_summary.tsv."
        )
        del name_to_count[unique_tsv]
    assert len(name_to_count) == 0, (
        "The following TSVs are listed in data/tsv_summary.tsv "
        "but could not be found in data/tsv: "
        f"{[name for name in name_to_count.keys()]}"
    )


def test_phones_data_matches_summary():
    """Check if each .phones file in data/phones is present in
    data/phones/phones_summary.tsv and if the number of phones in each .phones
    file matches its listed number of phones in data/phones_summary.tsv.

    (Basically checks whether generate_phones_summary.py has been run.)
    """
    name_to_count = {}
    with open(_PHONES_SUMMARY, "r", encoding="utf-8") as phones_summary:
        for line in phones_summary:
            language = line.rstrip().split("\t")
            name_to_count[language[0]] = int(language[-1])

    for phones_list in os.listdir(_PHONES_DIRECTORY):
        if phones_list.endswith(".phones"):
            with open(
                f"{_PHONES_DIRECTORY}/{phones_list}", "r", encoding="utf-8"
            ) as tsv:
                # We exclude blank lines and comments.
                num_of_entries = sum(
                    1
                    for line in tsv
                    if line.strip() and not line.startswith("#")
                )
            assert phones_list in name_to_count, (
                f"{phones_list} in data/phones but not in "
                "data/phones/phones_summary.tsv"
            )
            assert name_to_count[phones_list] == num_of_entries, (
                f"Number of entries in {phones_list} does not match "
                "number of entries in data/phones/phones_summary.tsv."
            )
            del name_to_count[phones_list]
    assert len(name_to_count) == 0, (
        "The following .phones files are listed in "
        "data/phones/phones_summary.tsv but could not be found in "
        f"data/phones: {[name for name in name_to_count.keys()]}"
    )
