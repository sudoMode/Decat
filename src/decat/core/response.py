#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A richer, public facing interface built on top of ``decat.core.model.Decat``.

``core.model.Decat`` remains untouched - it is purely responsible for
the scoring/ranking algorithm that produces tokens out of a deformed
string. This module wraps that model and:

    * times how long each extraction takes.
    * derives a "confidence" score for the extraction.
    * exposes a single-item processor that can be transparently
      parallelized (see ``decat.core.parallel``) to support bulk input.

The response schema is intentionally modeled as a small, extensible
dataclass (``DecatResponse``) so that new metrics can be bolted on in
the future without breaking the public dictionary contract.
"""

from dataclasses import dataclass, field
from time import perf_counter

from decat import __settings__ as settings
from decat.core.model import Decat
from decat.core.parallel import DEFAULT_EXECUTOR, parallelize


@dataclass
class DecatResponse:
    """
    Extensible response model for a single de-concatenation request.

    New metrics can be attached through ``extra`` without having to
    change the shape of this class, keeping the schema forward
    compatible.
    """

    results: list
    confidence: float
    elapsed: float
    extra: dict = field(default_factory=dict)

    def to_dict(self):
        payload = {
            "results": self.results,
            "confidence": self.confidence,
            "elapsed": self.elapsed,
        }
        payload.update(self.extra)
        return payload


def _new_client(language="en"):
    """
    Builds a brand new ``Decat`` client.

    A fresh client is used for every single-item invocation so that
    concurrent (thread/process based) executions never share mutable
    state, this is required since ``Decat`` keeps its working state on
    instance attributes.
    """
    return Decat(
        supported_languages=settings.SUPPORTED_LANGUAGES,
        vocabulary_map=settings.VOCABULARY_MAP,
        language=language,
    )


def _compute_confidence(client):
    """
    Derives a confidence score (0 -> 1) for the produced tokens.

    This purposefully does not touch/duplicate the cost based
    scoring/ranking mechanism implemented in ``core.model.Decat``. It
    simply reuses the vocabulary already loaded by the model to gauge
    what fraction of the produced tokens are recognised dictionary
    words, tokens that are not part of the vocabulary drag the
    confidence score down.
    """
    tokens = client.output
    if not tokens:
        return 0.0
    vocabulary = set(client.vocabulary)
    strip_chars = "".join(Decat.CHARACTERS_TO_PRESERVE)
    known = 0
    for token in tokens:
        normalized = token.strip(strip_chars).lower()
        if normalized in vocabulary:
            known += 1
    return round(known / len(tokens), 3)


@parallelize(default_executor=DEFAULT_EXECUTOR)
def process(target_string, preserve_special_characters=False, language="en"):
    """
    Single-item processor, decat's a single string and returns an
    enriched, dictionary based response (see ``DecatResponse``).

    This function is decorated with ``parallelize`` which transparently
    adds a ``.parallel(...)`` capability used by ``bulk_decat`` below to
    process many strings concurrently.
    """
    start = perf_counter()
    client = _new_client(language=language)
    client.preserve_special_characters = preserve_special_characters
    client.decat(target_string)
    elapsed = perf_counter() - start
    response = DecatResponse(
        results=client.output,
        confidence=_compute_confidence(client),
        elapsed=round(elapsed, 3),
    )
    return response.to_dict()


def bulk_decat(
    strings,
    preserve_special_characters=False,
    workers=None,
    executor=DEFAULT_EXECUTOR,
    language="en",
):
    """
    Public interface used to process multiple strings concurrently.

    :param strings: an iterable of deformed strings to process.
    :param preserve_special_characters: forwarded to ``Decat``.
    :param workers: number of threads/processes to use.
    :param executor: "thread" (default) or "process".
    :param language: forwarded to ``Decat``.
    :return: dict keyed by the original input string, each value
        being a dict with "results", "confidence" & "elapsed" keys.
    """
    return process.parallel(
        strings,
        workers=workers,
        executor=executor,
        preserve_special_characters=preserve_special_characters,
        language=language,
    )


__all__ = ["DecatResponse", "process", "bulk_decat"]
