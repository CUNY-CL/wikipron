#!/usr/bin/env python

import pynini
import pywrapfst as fst
import argparse
import logging


def main(args):
    with open(args.input_path, 'r') as source:  
        g_writer = fst.FarWriter.create(args.g_far_path)
        p_writer = fst.FarWriter.create(args.p_far_path)
        for (linenum, line) in enumerate(source, 1):
            key = f"{linenum:08x}"
            line = line.rstrip().split('\t')
            g = pynini.acceptor(line[0], token_type = args.token_type)
            g_compact = fst.convert(g, "compact_string")
            g_writer[key] = g_compact
            p = pynini.acceptor(line[1], token_type = args.token_type)
            p_compact = fst.convert(p, "compact_string")
            p_writer[key] = p_compact
        logging.info("Processed g and p pairs:\t%d pairs", linenum ) 
        
        
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input_path", required=True, help="Input path for grapheme and phoneme tsv file",
    )
    parser.add_argument(
        "--g_far_path", required=True, help="Outout grapheme FAR path"
    )
    parser.add_argument(
        "--p_far_path", required=True, help="Output phoneme FAR path"
    )
    parser.add_argument(
        "--token_type", required=True, help="token type for acceptors"
    )
    main(parser.parse_args())

