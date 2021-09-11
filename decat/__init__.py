from sys import version_info as version
from decat.__settings__ import SUPPORTED_LANGUAGES
from decat.__settings__ import VERSION
from decat.__settings__ import VOCABULARY_MAP
from decat.src import parse_user_args
from decat.src import Decat


major, minor, micro = version.major, version.minor, version.micro
required = 3.6
if float(f'{major}.{minor}') < required:
    print(f'Required Python >= {required}, detected: {major}.{minor}.{micro}')
    exit(0)

client = None


def decat(string):
    global client
    if client is None:
        client = Decat(supported_languages=SUPPORTED_LANGUAGES,
                       vocabulary_map=VOCABULARY_MAP)
    client.decat(string)
    return client.out


def print_version():
    print(f'Decat {VERSION}')


__all__ = [
            'decat',
            'parse_user_args',
            'print_version'
          ]
