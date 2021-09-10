from decat.__settings__ import VOCABULARY_MAP
from decat.__settings__ import SUPPORTED_LANGUAGES
from .model import Decat


client = Decat()


def decat(string):
    client.decat(string)
    return client.out


__all__ = ['VOCABULARY_MAP', 'SUPPORTED_LANGUAGES', 'decat']
