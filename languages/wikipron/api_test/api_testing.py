import wikipron
from language_samples import languages


for iso639_code in languages:
  phonemic_file = open(iso639_code + '.tsv', 'w')
  phonetic_file = open(iso639_code + '_phonetic' + '.tsv', 'w')

  config = wikipron.Config(key=iso639_code, casefold=True)
  for (word, pron) in wikipron.scrape(config):
    print(f"{word}\t{pron}", file=phonemic_file)

  phonetic_config = wikipron.Config(key=iso639_code, casefold=True, phonetic=True)
  for (word, pron) in wikipron.scrape(phonetic_config):
    print(f"{word}\t{pron}", file=phonetic_file)
  
  phonemic_file.close()
  phonetic_file.close()