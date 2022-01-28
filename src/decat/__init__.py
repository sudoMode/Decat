#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-

from sys import version_info as version

from decat import __settings__ as settings
from decat.core import Decat
from decat.parsers import parse_user_args

# check version compatibility
major, minor, micro = version.major, version.minor, version.micro
required = 3.6
if float(f'{major}.{minor}') < required:
    print(f'Required Python >= {required}, detected: {major}.{minor}.{micro}')
    exit(0)

# init client
client = Decat(supported_languages=settings.SUPPORTED_LANGUAGES,
               vocabulary_map=settings.VOCABULARY_MAP)


# decat user input
def decat(string, preserve_special_characters=False):
    client.preserve_special_characters = preserve_special_characters
    client.decat(string)
    return client.out


# allows for a CLI
def main():
    args = parse_user_args()
    if args.version:
        print(f'Decat {settings.VERSION}')
    if args.input:
        print(decat(args.input))


__all__ = [
            'main',
            'decat',
          ]


def test():
    print(decat('dummy.email@gmail.com'))


if __name__ == '__main__':
    test()
