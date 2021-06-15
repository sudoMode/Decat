# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path


__project__ = 'decat'
__description__ = """A Python package that provides the functionality
                     to de-concatenate a piece of text that does not have
                     any whitespaces in between."""
__author__ = 'Mandeep Singh'
__major__ = 1
__minor__ = 0
__micro__ = 0


VERSION = f'{__major__}.{__minor__}.{__micro__}'
BASE_DIR = Path(__file__).parent.parent
PROJECT_DIR = join(BASE_DIR, 'decat')
VOCABULARY_DIR = join(PROJECT_DIR, 'data', 'vocabulary')
