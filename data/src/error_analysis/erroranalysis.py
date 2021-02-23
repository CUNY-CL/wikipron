"""Error analysis tool for G2P.

This script assumes 2 input files. a) covering grammar b) test output.
CG file: Each line contain grapheme and their corresponding pronunciation
separated by a tab.
Test file: Contains three attributes in each line separated by a tab.
Example:
espresso ɛ s p ɹ ɛ s ə ʊ     ɛ k s p ɹ ɛ s ə ʊ
 """

__author__ = "Arundhati Sengupta"

import argparse

from prettytable import PrettyTable
import pynini


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
            # TODO: use Pynini's rewrite module here.
            lattice = (lg @ cg_fst @ pred_pron).project("output")
            if lattice.start() == pynini.NO_STATE_ID:
                if act == pred_pron:
                    not_rulematch_predmatch += 1
                else:
                    not_rulematch_pred_notmatch += 1
            elif act == pred_pron:
                rulematch_predmatch += 1
            else:
                rulematch_pred_notmatch += 1

    # Collecting the counts.
    rule_m_pred_nm = 100 * rulematch_pred_notmatch / total_records
    rule_m_pred_m = 100 * rulematch_predmatch / total_records
    rule_nm_pred_m = 100 * not_rulematch_predmatch / total_records
    rule_nm_pred_nm = 100 * not_rulematch_pred_notmatch / total_records

    # Building and printing the table
    rule_m_pred_nm_str = "{:05.2f}".format(rule_m_pred_nm)
    rule_m_pred_m_str = "{:05.2f}".format(rule_m_pred_m)
    rule_nm_pred_m_str = "{:05.2f}".format(rule_nm_pred_m)
    rule_nm_pred_nm_str = "{:05.2f}".format(rule_nm_pred_nm)

    print_table = PrettyTable()
    print_table.field_names = ["", "CG Match", "CG Not Match"]
    print_table.add_row(["Pron Match", rule_m_pred_m_str, rule_nm_pred_m_str])
    print_table.add_row(
        ["Pron Not Match", rule_m_pred_nm_str, rule_nm_pred_nm_str]
    )
    print(print_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cg_path", required=True, help="path to TSV covering grammar file"
    )
    parser.add_argument(
        "--test_path", required=True, help="path to test TSV file"
    )
    main(parser.parse_args())
