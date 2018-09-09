import csv
import re

LANG = 'Norwegian'

# Capture {comment}, <comment>, [comment].
regex = re.compile(r"(\s{.*}\s?)?(\s<.*>\s?)?(\s\[.*\]\s?)?$")


def idx_entry(nb, de, pos, comment, idx):
    print('<idx:entry name="{}" scriptable="yes" spell="yes">'.format(LANG))
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
    print('\t\t<p>{} {}</p>'.format(de, comment))
    print('\t</idx:short>')
    print('</idx:entry>')


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

with open('data/dict.cc_no-de.tsv', encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    idx = 1
    for row in reader:
        if len(row) < 2 or row[0].startswith('#'):
            continue
        nb = row[0].strip()
        de = row[1].strip()
        nb_word = re.sub(regex, "", nb)
        pos, comment = "", ""
        try:
            pos = '(' + row[2] + ')'
            comment = row[3]
        except IndexError:
            pass
        idx_entry(nb, de, pos, comment, idx)
        idx += 1


print('</mbp:frameset>')
print('</body>')
