import argparse

from collections import defaultdict
from random import choice

def main(args: argparse.Namespace):
	"""
	Wiktionary labels the pronunciations of <għ> as pharyngealization or as 
	/ɣ/ as "archaic" (although another source I found describes the  
	pronunciation as current but dialectal). To conform to Wiktionary, this 
	script weeds out any pronunciations of <għ> as pharyngealization or /ɣ/, 
	then randomly chooses from among the remaining pronunciations to write to
	the file.
	"""
	if not args.outfile:
		base = args.infile[:args.infile.rfind('.')]
		ext = args.infile[args.infile.rfind('.'):]
		args.outfile = base + "_gh_filtered" + ext

	with open(args.infile, 'r') as rf:
		with open(args.outfile, 'w') as wf:

			gh_dict = defaultdict(list)
			prev_gh = None

			for line in rf:
				word, pron = line.split('\t')

				# If the previous word is not a <għ> word...
				if prev_gh == None:
					if "għ" in word:
						if "ˤ" not in pron and "ɣ" not in pron:
							gh_dict[word].append(pron)

						prev_gh = word

					else:
						wf.write(line)

				# If the previous word is a <għ> word...
				else:
					# If we're still on the same word...
					if "għ" in word and word == prev_gh:
						if "ˤ" not in pron and "ɣ" not in pron:
							gh_dict[word].append(pron)

					
					# If we're on a different word, add the previous word to the
					# file
					else:
						# Write the previous word, if it has a valid 
						# pronunciation
						if len(gh_dict[prev_gh]) > 0:
							write_me = (prev_gh, choice(gh_dict[prev_gh]))
							write_me = '\t'.join(write_me)
							wf.write(write_me)
						gh_dict.clear()

						# If current word is a <għ> word, don't add it to
						# the file yet
						if "għ" in word:
							if "ˤ" not in pron and "ɣ" not in pron:
								gh_dict[word].append(pron)

							prev_gh = word

						# Otherwise, add the current word
						else:
							wf.write(line)
							prev_gh = None





if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("infile")
	parser.add_argument("-o", "--outfile")

	main(parser.parse_args())