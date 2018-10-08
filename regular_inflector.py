# Regular inflections for Norwegian nouns, verbs and adjectives.
from inflector import Inflector

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y', 'å', 'æ', 'ø']


class RegularInflector(Inflector):

    def inflect(self, entry):
        if entry.pos == '(noun)':
            return self.inflect_noun(entry.nb_word, entry.nb_comment)
        if entry.pos == '(verb)':
            return self.inflect_verb(entry.nb_word)
        if entry.pos == '(adj)':
            return self.inflect_adj(entry.nb_word)
        return set()

    def inflect_noun(self, nb_word, nb_comment):
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
            # We only need to add the DEF.SG declension.
            # The other declensions are identical to the masculine declensions,
            # and all feminine nouns are listed as {m/f} anyway.
            if nb_word.endswith('e'):
                inflections.add(nb_word[:-1] + 'a')  # DEF.SG
                inflections.add(nb_word[:-1] + 'as')  # DEF.SG.GEN
            else:
                inflections.add(nb_word + 'a')  # DEF.SG
                inflections.add(nb_word + 'as')  # DEF.SG.GEN
        if '{n' in nb_comment or 'n}' in nb_comment:
            # TODO monosyllabic et-words can have INDEF.PL forms
            # with a zero morpheme
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

    def inflect_verb(self, nb_word):
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

        if nb_word[-1] in VOWELS and not nb_word[-1] == 'e':
            stem = nb_word
        else:
            stem = nb_word[:-1]
            inflections.add(stem)  # IMP

        inflections.add(stem + 'ende')  # PRESP
        inflections.add(stem + 'es')  # PASS

        # Class 1
        if len(stem) > 2 and stem[-1] not in VOWELS and stem[-2] not in VOWELS:
            inflections.add(stem + 'et')  # PRET, PASTP
            inflections.add(stem + 'a')  # PRET, PASTP
        # Class 2
        elif len(stem) > 2 and stem[-1] not in VOWELS:
            inflections.add(stem + 'te')  # PRET
            inflections.add(stem + 't')  # PASTP
        # Class 3b
        elif len(stem) > 2 and \
                ((stem[-1] in VOWELS and stem[-2] in VOWELS) or
                 stem[-1] in ['v', 'g']):
            inflections.add(stem + 'de')  # PRET
            inflections.add(stem + 'd')  # PASTP
        # Class 3a
        else:
            inflections.add(stem + 'dde')  # PRET
            inflections.add(stem + 'dd')  # PASTP
        return inflections

    def inflect_adj(self, nb_word):
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
