import csv
import re

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

entries = {}
with open('data/dict.cc_no-de.tsv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        if len(row) < 2 or row[0].startswith('#'):
            continue
        nb = row[0].strip()
        de = row[1].strip()

        # If available, get additional information (POS tag, usage comments).
        pos, comment = "", ""
        try:
            pos = row[2].strip()
            if len(pos) > 0:
                pos = '(' + pos + ')'
            comment = row[3].strip()
            de = de + ' ' + comment
        except IndexError:
            pass

        # Merge entries for the same word.
        try:
            entries[(nb, pos)] += ', ' + de
        except KeyError:
            entries[(nb, pos)] = de

# Capture {comment}, <comment>, [comment].
regex = re.compile(r"(\s{.*}\s?)?(\s<.*>\s?)?(\s\[.*\]\s?)?$")


def idx_entry(nb, de, pos, idx):
    print('<idx:entry name="Norwegian" scriptable="yes" spell="yes">')
    print('\t<idx:short><a id="{}"/>'.format(idx))
    nb_comment = re.search(regex, nb)
    if nb_comment:
        nb_comment = nb_comment.group(0)
        nb_word = nb.replace(nb_comment, "")
    else:
        nb_word = nb
        nb_comment = ""
    print('\t\t<idx:orth value="{}">'.format(nb_word))
    print('\t\t\t<b>{}</b>{} {}'.format(nb_word, nb_comment, pos))
    # TODO inflection
    print('\t\t</idx:orth>')
    print('\t\t<p>{}</p>'.format(de))
    print('\t</idx:short>')
    print('</idx:entry>')


idx = 1
for (nb, pos), de in sorted(entries.items()):
    idx_entry(nb, de, pos, idx)
    idx += 1


print('</mbp:frameset>')
print('</body>')