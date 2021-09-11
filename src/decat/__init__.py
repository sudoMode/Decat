from sys import version_info as version
from decat.__settings__ import SUPPORTED_LANGUAGES
from decat.__settings__ import VERSION
from decat.__settings__ import VOCABULARY_MAP
from decat.parsers import parse_user_args
from decat.core import Decat


# check version compatibility
major, minor, micro = version.major, version.minor, version.micro
required = 3.6
if float(f'{major}.{minor}') < required:
    print(f'Required Python >= {required}, detected: {major}.{minor}.{micro}')
    exit(0)


# init client
client = Decat(supported_languages=SUPPORTED_LANGUAGES, vocabulary_map=VOCABULARY_MAP)


# decat user input
def decat(string):
    client.decat(string)
    return client.out


def print_version():
    print(f'Decat {VERSION}')


def hook():
    args = parse_user_args()
    if not(args.input or args.version):
        print('help menu')
    if args.version:
        print_version()
    if args.input:
        decat(args.input)


__all__ = [
            'hook',
            'decat',
          ]