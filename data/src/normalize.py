import argparse

from tempfile import TemporaryFile
from unicodedata import normalize

'''
normalize.py

Takes a file and normalizes it "in place." In order to avoid the issues of
reading and writing to the same file at the same time, this script puts the 
normalized version of the file argument in a tempfile, then uses that tempfile
to rewrite the original file.
'''

def main(args: argparse.Namespace) -> None:
	tf = TemporaryFile(mode='w+')

	with open(args.file, 'r') as rf:
		for line in rf:
			tf.write(normalize(args.norm, line))

	tf.seek(0)

	with open(args.file, 'w') as wf:
		for line in tf:
			wf.write(line)

	tf.close()



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Changes a file's unicode normalization")
	# File to normalize
	parser.add_argument("file", help="The file to modify")
	# Normalization type
	parser.add_argument("norm", choices=["NFC","NFD","NFKC","NFKD"], help="The type of normalization desired")

	main(parser.parse_args())