import re


# Capture {comment}, <comment>, [comment].
REGEX = re.compile(r"(\s{.*}\s?)?(\s<.*>\s?)?(\s\[.*\]\s?)?$")


class Entry():

    def __init__(self, nb, pos, de):
        nb_comment = re.search(REGEX, nb)
        if nb_comment:
            self.nb_comment = nb_comment.group(0)
            self.nb_word = nb.replace(self.nb_comment, "")
        else:
            self.nb_word = nb
            self.nb_comment = ""
        if pos == '(verb)' and self.nb_word[:2] != 'å ':
            self.nb_word = 'å ' + self.nb_word.strip()
        self.pos = pos
        self.de = de
        self.deps = []

    def add_dependent(self, entry):
        self.deps.append(entry)

    def title_string(self, tabs=True):
        s = '<b>{}</b>{} {}'.format(self.nb_word, self.nb_comment, self.pos)
        s = s.strip()
        return '\t\t\t' + s if tabs else s
