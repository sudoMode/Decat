from os import listdir
from os.path import dirname
from os.path import realpath
from os.path import join


CONTAINER_DIR = dirname(realpath(__file__))
SUPPORTED_LANGUAGES = list(filter(lambda x: x.isalpha(), listdir(CONTAINER_DIR)))
VOCABULARY_PATHS = list(map(lambda x: join(CONTAINER_DIR, x), SUPPORTED_LANGUAGES))
LANGUAGE_PATHS = dict(zip(SUPPORTED_LANGUAGES, VOCABULARY_PATHS))


def __validate(language):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f'Language {language} is not supported yet.')


def get_language_map(language='english'):
    __validate(language)
    language_path = LANGUAGE_PATHS.get(language)
    language_vocab = listdir(language_path)
    character_vocabs = list(filter(lambda x: x.endswith(r'.vocab'), language_vocab))
    language_map = {x.split('.')[0]: join(language_path, x) for x in character_vocabs}
    return language_map


def get_stop_words(language='english'):
    __validate(language)
    language_path = LANGUAGE_PATHS.get(language)
    stop_words = join(language_path, 'stop_words/stop_words.json')
    return stop_words



get_language_map('english')

