#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from decat import __settings__ as settings
from decat.core import Decat
from decat.core.parallel import DEFAULT_EXECUTOR
from decat.core.response import bulk_decat
from decat.parsers import load_inputs, parse_user_args

# init client
client = Decat(
    supported_languages=settings.SUPPORTED_LANGUAGES,
    vocabulary_map=settings.VOCABULARY_MAP,
)


# decat user input
def decat(
    string, preserve_special_characters=False, threads=None, executor=DEFAULT_EXECUTOR
):
    """
    De-concatenates the given input(s).

    Backward compatible behaviour: when ``string`` is a single ``str``,
    the original list of extracted tokens is returned, exactly as
    before.

    New behaviour: when ``string`` is an iterable of strings (e.g. a
    ``list`` or ``tuple``), every item is processed concurrently
    (see ``decat.core.parallel``) and a dictionary is returned, keyed
    by the original input string, each value holding the extracted
    ``results`` along with a ``confidence`` score and the ``elapsed``
    time it took to process it.

    :param string: a single string, or an iterable of strings.
    :param preserve_special_characters: preserve punctuation & other
        special characters in the output.
    :param threads: number of worker threads/processes to use when
        ``string`` is an iterable of strings. Defaults to the
        executor's own default sizing.
    :param executor: "thread" (default) or "process", only relevant
        when ``string`` is an iterable of strings.
    """
    if isinstance(string, str):
        client.preserve_special_characters = preserve_special_characters
        client.decat(string)
        return client.output
    return bulk_decat(
        string,
        preserve_special_characters=preserve_special_characters,
        workers=threads,
        executor=executor,
    )


# allows for a CLI
def main():
    args = parse_user_args()
    if args.version:
        print(f"Decat {settings.VERSION}")
    if args.input:
        inputs = load_inputs(args)
        if isinstance(inputs, str):
            print(
                decat(
                    inputs,
                    preserve_special_characters=args.preserve_special_chars,
                )
            )
        else:
            print(
                decat(
                    inputs,
                    preserve_special_characters=args.preserve_special_chars,
                    threads=args.threads,
                    executor=args.executor,
                )
            )


__all__ = [
    "main",
    "decat",
    "bulk_decat",
]
