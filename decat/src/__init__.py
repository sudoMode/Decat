from .__settings__ import *
from .core import Decat
from .parsers import parse_user_args


client = Decat(vocabulary_map=VOCABULARY_MAP, supported_languages=SUPPORTED_LANGUAGES)


def decat(string):
    client.decat(string)
    return client.out


__all__ = [
            'VERSION',
            'parse_user_args',
            'decat'
          ]
