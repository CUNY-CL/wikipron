"""Error analysis tool for G2P.

This script assumes 2 input files. a) covering grammar b) test output.
CG file: Each line contain grapheme and their corresponding pronunciation
separated by a tab.
Test file: contains three attributes in each line separated by a tab.
Example: espresso ɛ s p ɹ ɛ s ə ʊ     ɛ k s p ɹ ɛ s ə ʊ
 """

__author__ = "Arundhati Sengupta"

import pynini
import argparse
from prettytable import PrettyTable


def main(args: argparse.Namespace) -> None:
    cg_fst = pynini.string_file(args.cg_path).closure().optimize()
    rulematch_predmatch = 0
    rulematch_pred_notmatch = 0
    not_rulematch_predmatch = 0
    not_rulematch_pred_notmatch = 0
    total_records = 0
    with open(args.test_path, "r") as source:
        for line in source:
            total_records += 1
            parts = line.split("\t")
            lg = parts[0].strip()
            act = parts[1].replace(" ", "").replace(".", "").strip()
            pred_pron = parts[2].replace(" ", "").replace(".", "").strip()
            lattice = (ben @ bn_fst @ predPron).project("output")
            if lattice.start() == pynini.NO_STATE_ID:
                if act == pred_pron:
                    not_rulematch_predmatch += 1
                else:
                    not_rulematch_pred_notmatch += 1
            else:
                if act == pred_pron:
                    rulematch_predmatch += 1
                else:
                    rulematch_pred_notmatch += 1

    print("Total Number of Records", total_records)
    rule_m_pred_nm = (rulematch_pred_notmatch / total_records) * 100
    rule_m_pred_m = (rulematch_predmatch / total_records) * 100
    rule_nm_pred_m = (not_rulematch_predmatch / total_records) * 100
    rule_nm_pred_nm = (not_rulematch_pred_notmatch / total_records) * 100

    printtable(rule_m_pred_nm, rule_m_pred_m, rule_nm_pred_m, rule_nm_pred_nm)


def printtable(rule_m_pred_nm, rule_m_pred_m, rule_nm_pred_m, rule_nm_pred_nm):
    rule_m_pred_nm = "{:05.2f}".format(rule_m_pred_nm)
    rule_m_pred_m = "{:05.2f}".format(rule_m_pred_m)
    rule_nm_pred_m = "{:05.2f}".format(rule_nm_pred_m)
    rule_nm_pred_nm = "{:05.2f}".format(rule_nm_pred_nm)

    # printing the result in a table
    x = PrettyTable()

    x.field_names = ["", "CG Match", "CG Not Match"]

    x.add_row(["Pron Match", rule_m_pred_m, rule_nm_pred_m])
    x.add_row(["Pron Not Match", rule_m_pred_nm, rule_nm_pred_nm])

    print(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cg_path", required=True, help="path to TSV covering grammar file"
    )
    parser.add_argument(
        "--test_path", required=True, help="path to test tsv file"
    )
    main(parser.parse_args())
