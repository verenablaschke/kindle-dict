import csv
import re
from entry import Entry
from regular_inflector import RegularInflector
from spraakbanken_inflector import SpraakbankenInflector


EXACT_MATCH_CHARS = ['Å', 'å', 'Ø', 'ø', 'Æ', 'æ']
EXACT_MATCH_STR = ' exact="yes"'

# XHTML necessary for MOBI conversion
print('<html')
print('xmlns:math="http://exslt.org/math"')
print('xmlns:svg="http://www.w3.org/2000/svg"')
print('xmlns:tl="https://kindlegen.s3.amazonaws.com/'
      'AmazonKindlePublishingGuidelines.pdf"')
print('xmlns:saxon="http://saxon.sf.net/"')
print('xmlns:xs="http://www.w3.org/2001/XMLSchema"')
print('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
print('xmlns:cx="https://kindlegen.s3.amazonaws.com/'
      'AmazonKindlePublishingGuidelines.pdf"')
print('xmlns:dc="http://purl.org/dc/elements/1.1/"')
print('xmlns:mbp="https://kindlegen.s3.amazonaws.com/'
      'AmazonKindlePublishingGuidelines.pdf"')
print('xmlns:mmc="https://kindlegen.s3.amazonaws.com/'
      'AmazonKindlePublishingGuidelines.pdf"')
print('xmlns:idx="https://kindlegen.s3.amazonaws.com/'
      'AmazonKindlePublishingGuidelines.pdf">')
print('<head>')
print('\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
print('</head>')
print('<body>')
print('<mbp:frameset>')

# Read the dict.cc entries.
entries = {}
pos_tags = set()
with open('data/dict.cc/dict.cc.tsv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if len(row) < 2 or row[0].startswith('#'):
            continue
        nb = row[0].strip()
        nb = nb.replace(' [kvinnelig]', '')
        de = row[1].strip()

        # If available, get additional information (POS tag, usage comments).
        pos, comment = "", ""
        try:
            pos = row[2].strip()
            if len(pos) > 0:
                if pos == 'verb' and nb[:2] == 'å ':
                    nb = nb[2:]
                pos = '(' + pos + ')'
                pos_tags.add(pos)
            comment = row[3].strip()
            if len(comment) > 0:
                de = de + ' ' + comment
        except IndexError:
            pass

        # Add the entry.
        # Merge entries for the same word.
        try:
            entries[(nb, pos)] += ', ' + de
        except KeyError:
            entries[(nb, pos)] = de

# Get the stopwords.
stop_words = set()
with open('data/stopwords/stopwords.txt', encoding='utf8') as f:
    for l in f:
        stop_words.add(l.strip())

# Differentiate between single-token and multi-token entries.
entries_single = {}
entries_multi = {}
for (nb, pos), de in entries.items():
    entry = Entry(nb, pos, de)
    if len(entry.nb_word.split()) == 1:
        # When possible without clashes, index the entries by their actual
        # tokens (without comments). It's not perfect, but it makes it easy
        # and quick to identify single-token entries later on.
        try:
            entries_single[(entry.nb_word, pos)]
            entries_single[(nb, pos)] = entry
        except KeyError:
            entries_single[(entry.nb_word, pos)] = entry
    else:
        entries_multi[(nb, pos)] = entry

# Add information about multi-token entries to the individual tokens' entries.
symbols = re.compile(r'[^\w]')
for _, entry_multi in entries_multi.items():
    for tok in entry_multi.nb_word.split():
        tok = re.sub(symbols, '', tok)
        if tok not in stop_words:
            for pos in pos_tags:
                try:
                    entry_single = entries_single[(tok, pos)]
                    entry_single.add_dependent(entry_multi)
                    entries_single[(tok, pos)] = entry_single
                except KeyError:
                    pass

# Instantiate the inflectors.
inflector_reg = RegularInflector()
inflector_spr = SpraakbankenInflector()


# Write the entries.
def idx_entry(entry, idx):
    print('<idx:entry name="Norwegian" scriptable="yes" spell="yes">')
    print('\t<idx:short><a id="{}"/>'.format(idx))
    # If the entry contains special characters, try to make sure they are taken
    # into account when the word is being looked up.
    # (Not entirely sure how much this is actually taken into consideration
    # when using the dictionary.)
    exact_match = False
    for c in entry.nb_word:
        if c in EXACT_MATCH_CHARS:
            exact_match = True
            break
    print('\t\t<idx:orth value="{}"{}>'
          .format(entry.nb_word,
                  EXACT_MATCH_STR if exact_match else ''))
    print(entry.title_string())

    # Inflected forms.
    if pos:
        inflections = inflector_spr.inflect(entry)
        # If it's not in the Språkbanken file, generate regularly inflected
        # forms:
        if not inflections:
            inflections = inflector_reg.inflect(entry)
        if inflections:
            print('\t\t\t<idx:infl>')
            for infl in inflections:
                print('\t\t\t\t<idx:iform value="{}"{}/>'
                      .format(infl,
                              EXACT_MATCH_STR if exact_match else ''))
            print('\t\t\t</idx:infl>')

    print('\t\t</idx:orth>')
    print('\t\t<p>{}</p>'.format(entry.de))
    if entry.deps:
        print('\t\t<ul>')
        for dep in sorted(entry.deps, key=lambda x: x.nb_word):
            print('\t\t\t<li>{}: {}</li>'.format(dep.title_string(tabs=False),
                                                 dep.de))
        print('\t\t</ul>')
    print('\t</idx:short>')
    print('</idx:entry>')


idx = 1
for entry in entries_single.values():
    idx_entry(entry, idx)
    idx += 1
for entry in entries_multi.values():
    idx_entry(entry, idx)
    idx += 1

# Close open HTML tags.
print('</mbp:frameset>')
print('</body>')
