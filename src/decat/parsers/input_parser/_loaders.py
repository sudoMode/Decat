#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers used to load bulk input(s) for decat from a file.

New file types can be plugged into ``LOADERS`` without having to touch
the CLI parsing logic or ``decat``'s core processing pipeline.
"""

from json import loads


def _load_json(path):
    """
    Loads a list of strings to be de-concatenated from a JSON file.

    Supported JSON shapes:
        * a flat JSON array of strings, e.g. ``["str1", "str2"]``
        * a JSON object with an "input" key holding a list of strings,
          e.g. ``{"input": ["str1", "str2"]}``
    """
    with open(path, "r") as f:
        payload = loads(f.read())
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "input" in payload:
        return payload["input"]
    raise ValueError(
        f'Unsupported JSON structure in "{path}", expected either a list of '
        f'strings or an object with an "input" key holding a list of strings.'
    )


LOADERS = {
    "json": _load_json,
}


def load_from_file(paths, file_type):
    """
    Loads and merges the strings to be de-concatenated from one or more
    files of the given ``file_type``.
    """
    loader = LOADERS.get(file_type)
    if loader is None:
        raise ValueError(
            f'Unsupported file type "{file_type}", pick from: {list(LOADERS.keys())}'
        )
    strings = []
    for path in paths:
        strings.extend(loader(path))
    return strings


__all__ = ["load_from_file", "LOADERS"]
