# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path

# version
__major__ = 1
__minor__ = 0
__micro__ = 0


VERSION = f'{__major__}.{__minor__}.{__micro__}'
BASE = Path(__file__).parent.parent.parent.resolve()
PROJECT = join(BASE, 'decat')
SOURCE = join(PROJECT, 'src')
DATA = join(PROJECT, '.data')
VOCABULARY = join(DATA, 'vocabulary')
SUPPORTED_LANGUAGES = dict(english='en')
VOCABULARY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(VOCABULARY, x, 'tokens.json'),
                              SUPPORTED_LANGUAGES.values())))
_FREQUENCY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(VOCABULARY, x, 'frequency.json'),
                              SUPPORTED_LANGUAGES.values())))
