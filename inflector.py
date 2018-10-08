from abc import ABC, abstractmethod


class Inflector(ABC):

    @abstractmethod
    def inflect(self, entry):
        pass
