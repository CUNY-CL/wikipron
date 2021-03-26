#!/usr/bin/env python
"""Creates covering grammar FST from TSV of correspondences."""

import argparse

import pynini


TOKEN_TYPES = ["byte", "utf8"]


def main(args: argparse.Namespace) -> None:
    input_token_type = (
        args.input_token_type
        if args.input_token_type in TOKEN_TYPES
        else pynini.SymbolTable.read_text(args.input_token_type)
    )
    output_token_type = (
        args.output_token_type
        if args.output_token_type in TOKEN_TYPES
        else pynini.SymbolTable.read_text(args.output_token_type)
    )
    cg = pynini.string_file(
        args.tsv_path,
        input_token_type=input_token_type,
        output_token_type=output_token_type,
    )
    cg.closure().optimize()
    cg.write(args.fst_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input_token_type",
        default="utf8",
        help="input token type or path to symbol table (default: %(default)s)",
    )
    parser.add_argument(
        "--output_token_type",
        default="utf8",
        help="output token type or path to symbol table "
        "(default: %(default)s)",
    )
    parser.add_argument("tsv_path", help="path to input TSV")
    parser.add_argument("fst_path", help="path to output FST")
    main(parser.parse_args())
