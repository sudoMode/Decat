#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-


from decat import __settings__ as settings
from decat.core import Decat
from decat.parsers import parse_user_args


# init client
client = Decat(supported_languages=settings.SUPPORTED_LANGUAGES,
               vocabulary_map=settings.VOCABULARY_MAP)


# decat user input
def decat(string, preserve_special_characters=False):
    client.preserve_special_characters = preserve_special_characters
    client.decat(string)
    return client.output


# allows for a CLI
def main():
    args = parse_user_args()
    if args.version:
        print(f'Decat {settings.VERSION}')
    if args.input:
        print(decat(args.input,
                    preserve_special_characters=args.preserve_special_chars))


__all__ = [
    'main',
    'decat',
]


def test():
    target = 'dummy.email@gmail.com'
    print('Standard conversion...')
    print(f'Target: {target} | Results: {decat(target)}')
    print('\nPreserving special characters...')
    print(f'Target: {target} | Results: '
          f'{decat(target, preserve_special_characters=True)}')


if __name__ == '__main__':
    test()
