from abc import ABC, abstractmethod


class Inflector(ABC):

    @abstractmethod
    def inflect(self, nb_word, nb_comment, pos):
        pass
