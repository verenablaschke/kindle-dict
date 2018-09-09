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
            if len(comment) > 0:
                de = de + ' ' + comment
        except IndexError:
            pass

        # Merge entries for the same word.
        try:
            entries[(nb, pos)] += ', ' + de
        except KeyError:
            entries[(nb, pos)] = de


def inflect_noun(nb_word, nb_comment):
    inflections = set()
    # TODO entries consisting of more than one word
    if len(nb_word.split()) > 1:
        return inflections
    if '{m' in nb_comment or 'm}' in nb_comment:
        if nb_word.endswith('e'):
            inflections.add(nb_word + 'n')  # DEF.SG
            inflections.add(nb_word + 'ns')  # DEF.SG.GEN
            inflections.add(nb_word + 'r')  # INDEF.PL
            inflections.add(nb_word + 'ne')  # DEF.PL
            inflections.add(nb_word + 'nes')  # DEF.PL.GEN
        else:
            inflections.add(nb_word + 'en')  # DEF.SG
            inflections.add(nb_word + 'ens')  # DEF.SG.GEN
            inflections.add(nb_word + 'er')  # INDEF.PL
            inflections.add(nb_word + 'ene')  # DEF.PL
            inflections.add(nb_word + 'enes')  # DEF.PL.GEN
    if '{f' in nb_comment or 'f}' in nb_comment:
        # We only need to add the DEF.SG declension. The other declensions
        # are identical to the masculine declensions, and all feminine nouns
        # are listed as {m/f} anyway.
        if nb_word.endswith('e'):
            inflections.add(nb_word[:-1] + 'a')  # DEF.SG
            inflections.add(nb_word[:-1] + 'as')  # DEF.SG.GEN
        else:
            inflections.add(nb_word + 'a')  # DEF.SG
            inflections.add(nb_word + 'as')  # DEF.SG.GEN
    if '{n' in nb_comment or 'n}' in nb_comment:
        # TODO
        # monosyllabic et-words can have INDEF.PL forms with a zero morpheme
        if nb_word.endswith('e'):
            inflections.add(nb_word + 't')  # DEF.SG
            inflections.add(nb_word + 'ts')  # DEF.SG.GEN
            inflections.add(nb_word + 'r')  # INDEF.PL
            inflections.add(nb_word + 'ne')  # DEF.PL
            inflections.add(nb_word[:-1] + 'a')  # DEF.PL
            inflections.add(nb_word + 'nes')  # DEF.PL.GEN
            inflections.add(nb_word[:-1] + 'as')  # DEF.PL.GEN
        else:
            inflections.add(nb_word + 'et')  # DEF.SG
            inflections.add(nb_word + 'ets')  # DEF.SG.GEN
            inflections.add(nb_word + 'er')  # INDEF.PL
            inflections.add(nb_word + 'ene')  # DEF.PL
            inflections.add(nb_word + 'a')  # DEF.PL
            inflections.add(nb_word + 'enes')  # DEF.PL.GEN
            inflections.add(nb_word + 'as')  # DEF.PL.GEN
    return inflections


vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'å', 'æ', 'ø']


def inflect_verb(nb_word):
    if nb_word.startswith('å '):
        nb_word = nb_word.replace('å ', '')

    inflections = set()
    # TODO entries consisting of more than one word
    # TODO entries of type 'verb + preposition'
    if len(nb_word.split()) > 1:
        return inflections

    if nb_word.endswith('s'):
        return inflections

    inflections.add(nb_word + 'r')  # PRES

    if nb_word[-1] in vowels and not nb_word[-1] == 'e':
        stem = nb_word
    else:
        stem = nb_word[:-1]
        inflections.add(stem)  # IMP

    inflections.add(stem + 'ende')  # PRESP
    inflections.add(stem + 'es')  # PASS

    # Class 1
    if len(stem) > 2 and stem[-1] not in vowels and stem[-2] not in vowels:
        inflections.add(stem + 'et')  # PRET, PASTP
        inflections.add(stem + 'a')  # PRET, PASTP
    # Class 2
    elif len(stem) > 2 and stem[-1] not in vowels:
        inflections.add(stem + 'te')  # PRET
        inflections.add(stem + 't')  # PASTP
    # Class 3b
    elif len(stem) > 2 and \
            ((stem[-1] in vowels and stem[-2] in vowels) or
             stem[-1] in ['v', 'g']):
        inflections.add(stem + 'de')  # PRET
        inflections.add(stem + 'd')  # PASTP
    # Class 3a
    else:
        inflections.add(stem + 'dde')  # PRET
        inflections.add(stem + 'dd')  # PASTP
    return inflections


def inflect_adj(nb_word):
    inflections = set()
    # TODO entries consisting of more than one word
    if len(nb_word.split()) > 1:
        return inflections

    if nb_word[-2:] in ['sk', 'ig']:
        inflections.add(nb_word + 't')  # N

    if nb_word[-2:] in ['en', 'el', 'er']:
        stem = nb_word[:-2] + nb_word[-1]
        # gammel -> gamle, vakker -> vakre
        if len(stem) > 3 and stem[-2] == stem[-3]:
            stem = stem[:-3] + stem[-2:]
    else:
        stem = nb_word
    inflections.add(stem + 'e')  # PL, DEF

    # TODO which adjectives use mer/mest instead?
    inflections.add(stem + 'ere')  # COMP
    if stem.endswith('ig'):
        inflections.add(stem + 'st')  # INDEF.SUP
        inflections.add(stem + 'ste')  # DEF.SUP
    else:
        inflections.add(stem + 'est')  # INDEF.SUP
        inflections.add(stem + 'este')  # DEF.SUP
    return inflections


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

    # Inflected forms.
    if pos:
        print('\t\t\t<idx:infl>')
        inflections = []
        if pos == '(noun)':
            inflections = inflect_noun(nb_word, nb_comment)
        elif pos == '(verb)':
            inflections = inflect_verb(nb_word)
        elif pos == '(adj)':
            inflections = inflect_adj(nb_word)
        for infl in inflections:
            print('\t\t\t\t<idx:iform value="{}"/>'.format(infl))
        print('\t\t\t</idx:infl>')

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
