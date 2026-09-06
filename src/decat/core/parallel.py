#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic, resuable parallel-processing decorator.

The goal of this module is to decouple "parallelization" from any
particular piece of business logic. Any function that knows how to
process a *single* item can be decorated with ``parallelize`` and it
will automatically gain the ability to process a *collection* of items
concurrently, either using a pool of threads or a pool of processes.

This keeps the core extraction logic (``decat.core.model.Decat``)
completely untouched while still allowing bulk / concurrent processing
to be layered on top of it (or on top of any other single-item
callable in the future).
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import wraps

# Registry of supported execution engines. New engines (e.g. asyncio based)
# can be plugged in here without touching the decorator implementation.
EXECUTORS = {
    "thread": ThreadPoolExecutor,
    "process": ProcessPoolExecutor,
}

DEFAULT_EXECUTOR = "thread"


def _resolve_executor(executor):
    """
    Resolve a user supplied executor identifier (or executor class) into
    a concrete ``concurrent.futures.Executor`` subclass.
    """
    if executor in EXECUTORS:
        return EXECUTORS[executor]
    if isinstance(executor, type):
        return executor
    raise ValueError(
        f'Unsupported executor "{executor}", pick from: {list(EXECUTORS.keys())}'
    )


def parallelize(default_workers=None, default_executor=DEFAULT_EXECUTOR):
    """
    Decorator factory that adds bulk/parallel processing capabilities to
    any single-item callable.

    The decorated function keeps working exactly as before when called
    directly, i.e. ``function(item, *args, **kwargs)``.

    Additionally, the decorated function exposes a ``.parallel(...)``
    helper that fans a collection of items out across a pool of workers
    (threads by default, processes optionally) and gathers the results
    back into a dictionary keyed by the original input item.

    Usage::

        @parallelize()
        def process(item):
            ...

        results = process.parallel(["item-1", "item-2"], workers=4)
        # {"item-1": result_1, "item-2": result_2}
    """

    def decorator(func):
        @wraps(func)
        def wrapper(item, *args, **kwargs):
            return func(item, *args, **kwargs)

        def run_parallel(
            items, workers=default_workers, executor=default_executor, *args, **kwargs
        ):
            """
            Run ``func`` for every item in ``items`` concurrently.

            :param items: an iterable of items to process.
            :param workers: number of worker threads/processes to use,
                defaults to the executor's own default sizing when None.
            :param executor: either "thread", "process" or a custom
                ``concurrent.futures.Executor`` subclass.
            :return: a dict mapping every input item to the result
                produced by ``func`` for that item.
            """
            items = list(items)
            executor_cls = _resolve_executor(executor)
            results = {}
            with executor_cls(max_workers=workers) as pool:
                futures = {
                    pool.submit(wrapper, item, *args, **kwargs): item for item in items
                }
                for future, item in futures.items():
                    results[item] = future.result()
            return results

        wrapper.parallel = run_parallel
        return wrapper

    return decorator


__all__ = ["parallelize", "EXECUTORS", "DEFAULT_EXECUTOR"]
