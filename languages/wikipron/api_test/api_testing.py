import wikipron
from language_samples import languages

readme_string = '''
| Link | ISO 639-2 Code | ISO 639 Language Name | Wiktionary Language Name | Case-folding | Phonetic/Phonemic | # of entries |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
'''

for iso639_code in languages:
  if iso639_code != 'baq':
    break
  phonemic_iterator = 0
  phonemic_file = open(iso639_code + '.tsv', 'w')
  phonetic_iterator = 0
  phonetic_file = open(iso639_code + '_phonetic' + '.tsv', 'w')

  config = wikipron.Config(key=iso639_code, casefold=languages[iso639_code]['casefold'])
  for (word, pron) in wikipron.scrape(config):
    phonemic_iterator += 1
    print(f"{word}\t{pron}", file=phonemic_file)

  phonetic_config = wikipron.Config(key=iso639_code, casefold=languages[iso639_code]['casefold'], phonetic=True)
  for (word, pron) in wikipron.scrape(phonetic_config):
    phonetic_iterator += 1
    print(f"{word}\t{pron}", file=phonetic_file)
  
  row = ['Link details', iso639_code, languages[iso639_code]['iso639_name'], languages[iso639_code]['wiktionary_name'], str(languages[iso639_code]['casefold']), 'Phonemic', str(phonemic_iterator)]
  # Simplify this step later
  if phonetic_iterator >= phonemic_iterator:
    row[5] = 'Phonetic'
    row[6] = phonemic_iterator

  readme_string += '| ' + ' | '.join(row) + ' |'
  # Obviously not ideal if actually iterating
  with open('readme_test.md', 'w') as file:
    file.write(readme_string)
  phonemic_file.close()
  phonetic_file.close()
