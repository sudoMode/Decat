# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path


__project__ = 'decat'
__description__ = """De-concatenate strings without white-spaces."""
__author__ = 'Mandeep Singh'
__major__ = 1
__minor__ = 0
__micro__ = 0


VERSION = f'{__major__}.{__minor__}.{__micro__}'
BASE = Path(__file__).parent.parent
PROJECT = join(BASE, 'decat')
_VOCABULARY = join(PROJECT, '.data', 'vocabulary')
SUPPORTED_LANGUAGES = dict(english='en')
VOCABULARY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(_VOCABULARY, x, 'tokens.json'),
                              SUPPORTED_LANGUAGES.values())))
_FREQUENCY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(_VOCABULARY, x, 'frequency.json'),
                              SUPPORTED_LANGUAGES.values())))
