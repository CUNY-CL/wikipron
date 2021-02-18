"""Error Analysis tool for G2P.

This script assumes 2 input files. a) Covering Grammer b) Test output. 
CG file  : Each line contain graphime and their corresponding pronunciation seperated by a tab
Test File: contains three attributes in each line seperated by a tab. The attributes are - orthography, expected pronunciation, and hypothesized pronunciation."""

__author__ = "Arundhati Sengupta"

import pynini
import argparse

def main(args: argparse.Namespace):
    cg_fst = pynini.string_file(args.cg_path).closure().optimize()
    rulematch_predMatch = 0
    rulematch_predNotMatch = 0
    notRulematch_predMatch = 0
    notRulematch_predNotMatch = 0
    total_records = 0
    with open(args.test_path, "r") as source:
        for line in source:
            total_records+=1
            parts = line.split('\t')
            lg = parts[0].strip()
            act = parts[1].replace(' ','').replace('.','').strip()
            predPron = parts[2].replace(' ','').replace('.','').strip()
             
            lattice = (lg @ cg_fst @ predPron).project(True)
            
            if lattice.start() == pynini.NO_STATE_ID:
                if (act == predPron):
                    notRulematch_predMatch += 1
                    
                else:
                    notRulematch_predNotMatch += 1            
            else:
                if (act == predPron):
                    rulematch_predMatch += 1
                else:
                    rulematch_predNotMatch += 1
    
    print ('Total Number of Records', total_records)
    ruleMpredNM = round(rulematch_predNotMatch / total_records, 4) * 100
    ruleMpredM = round(rulematch_predMatch / total_records, 4) * 100
    ruleNMpredM = round (notRulematch_predMatch / total_records, 4) * 100
    ruleNMpredNM = round(notRulematch_predNotMatch / total_records, 4) * 100

    printtable(ruleMpredNM, ruleMpredM,ruleNMpredM,ruleNMpredNM)


def printtable(ruleMpredNM, ruleMpredM,ruleNMpredM,ruleNMpredNM):
    ruleMpredNM = '{:05.2f}'.format(ruleMpredNM)
    ruleMpredM = '{:05.2f}'.format(ruleMpredM)
    ruleNMpredM = '{:05.2f}'.format(ruleNMpredM)
    ruleNMpredNM = '{:05.2f}'.format(ruleNMpredNM)

    print('                                            ')
    print('               | CG Match  |   CG Not Match |')
    print('---------------|-----------+----------------|')
    print('Pron Match     | ',ruleMpredM,'   |     ',ruleNMpredM,'    |')
    print('Pron Not Match | ',ruleMpredNM,'   |     ',ruleNMpredNM,'    |')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cg_path", required=True, help="path to file of covering grammar which is a tsv file. Each line contain graphime and their corresponding pronunciation seperated by a tab"
    )
    parser.add_argument(
        "--test_path", required=True, help="path to test tsv file which contains three attributes in each line seperated by a tab. The attributes are - orthography, expected pronunciation, and hypothesized pronunciation."
    )
    main(parser.parse_args())