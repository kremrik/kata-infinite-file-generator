import csv
import json
from functools import partial
from typing import Callable, Generator, IO, Iterator


__all__ = ["inf_csv", "inf_json_lines", "inf_text"]


def inf_csv(handler: IO, header: bool) -> Generator:
    processor = partial(_generate_csv, header=header)
    yield from gen_loop(handler, processor)


def inf_json_lines(handler: IO) -> Generator:
    yield from gen_loop(handler, _generate_json)


def inf_text(handler: IO) -> Generator:
    yield from gen_loop(handler, _generate_text)


# ---------------------------------------------------------
def gen_loop(
    handler: IO, processor: Callable[[IO], Generator]
) -> Generator:
    while 1:
        yield from processor(handler)
        handler.seek(0)


# ---------------------------------------------------------
def _generate_csv(
    handler: Iterator, header: bool
) -> Generator:
    reader = csv.reader(handler)

    if header:
        next(reader)

    for row in reader:
        yield row

def _generate_json(handler: IO) -> Generator:
    for j in handler:
        yield json.loads(j)


def _generate_text(handler: IO) -> Generator:
    for t in handler:
        yield t.rstrip()
