import csv
from inflector import Inflector

POS2TAG = {'(noun)': 'subst', '(verb)': 'verb', '(adj)': 'adj'}


class SpraakbankInflector(Inflector):
    __slots__ = 'lemma2inflections'

    def __init__(self):
        id2lemma = {}
        with open('data/spraakbanken/lemma.txt', encoding='utf8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                id2lemma[row['LEMMA_ID'].strip()] = row['GRUNNFORM'].strip()

        self.lemma2inflections = {}
        with open('data/spraakbanken/fullformsliste.txt', encoding='utf8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                try:
                    key = (id2lemma[row['LEMMA_ID'].strip()],
                           row['TAG'].strip().split()[0])
                except KeyError:
                    continue
                val = row['OPPSLAG'].strip()
                try:
                    self.lemma2inflections[key].add(val)
                except KeyError:
                    self.lemma2inflections[key] = {val}
                # TODO genitive

    def inflect(self, nb_word, nb_comment, pos):
        if pos == '(verb)' and nb_word.startswith('å '):
            nb_word = nb_word.replace('å ', '')
        try:
            return self.lemma2inflections[(nb_word, POS2TAG[pos])]
        except KeyError:
            return set()
