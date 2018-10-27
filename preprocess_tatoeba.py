import csv
import tarfile
import codecs

PATH_TATOEBA = 'data/tatoeba/'
# ISO 639-3 codes. NOR = Norwegian (any variety), NOB = Bokmål
NOR = ['nor', 'nob']
OTHER = ['eng', 'deu']

# Map idx -> sentence
sentences_nor = {}
sentences_other = {}

# Extract the relevant sentences.
tar = tarfile.open(PATH_TATOEBA + 'sentences.tar.bz2', 'r:bz2')
for member in tar.getmembers():
    f = tar.extractfile(member)
    reader = csv.reader(codecs.iterdecode(f, 'utf-8'), delimiter='\t')
    for row in reader:
        idx, lang, sentence = int(row[0]), row[1].lower(), row[2]
        if lang in NOR:
            sentences_nor[idx] = sentence
            continue
        if lang in OTHER:
            sentences_other[idx] = sentence
tar.close()

print(list(sentences_nor.items())[:5])
print(list(sentences_other.items())[:5])

sorted_ids = sorted(list(sentences_nor.items()))
idx_min = sorted_ids[0][0]
idx_max = sorted_ids[-1][0]
del sorted_ids
print('min', idx_min, 'max', idx_max)

# Extract links to translations.
sentences = {}  # idx -> [sentences_nor, sentence_translated, length].
tar = tarfile.open(PATH_TATOEBA + 'links.tar.bz2', 'r:bz2')
for member in tar.getmembers():
    f = tar.extractfile(member)
    reader = csv.reader(codecs.iterdecode(f, 'utf-8'), delimiter='\t')
    prev_idx = -1
    for row in reader:
        idx = int(row[0])
        # Fortunately, the rows are in order.
        # Skip translations for non-Norwegian sentences.
        if idx < idx_min or idx > idx_max:
            continue
        try:
            sent_transl = sentences_other[int(row[1])]
            length = len(sent_transl.split())
            try:
                # Allow only one translation per sentence;
                # pick the shortest one.
                length_prev = sentences[idx][2]
                if length >= length_prev:
                    continue
            except KeyError:
                pass
            sentences[idx] = [sentences_nor[idx], sent_transl, length]
        except KeyError:
            # Doesn't have a translation in one of the languages in OTHER.
            pass
tar.close()

del sentences_nor
del sentences_other

print(list(sentences.items())[:5])
