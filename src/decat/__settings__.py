# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path

# version
__major__ = 0
__minor__ = 0
__micro__ = 6


VERSION = f'{__major__}.{__minor__}.{__micro__}-alpha'
BASE = Path(__file__).parent.resolve()
DATA = join(BASE, '.data')
VOCABULARY = join(DATA, 'vocabulary')
SUPPORTED_LANGUAGES = dict(english='en')
VOCABULARY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(VOCABULARY, x, 'tokens.json'),
                              SUPPORTED_LANGUAGES.values())))
_FREQUENCY_MAP = dict(zip(SUPPORTED_LANGUAGES.values(),
                          map(lambda x: join(VOCABULARY, x, 'frequency.json'),
                              SUPPORTED_LANGUAGES.values())))