import itertools
import multiprocessing
import os
import re
from dataclasses import dataclass
from typing import Pattern, Generator


@dataclass
class Counter:
    sentence_count: int = 0
    chars_count: int = 0
    num_of_words_count: int = 0
    max_letters_count: int = 0
    spec_symbols_count: int = 0

    def __add__(self, other_inst):
        if not isinstance(other_inst, Counter):
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'"
                .format(type(self).__name__, type(other_inst).__name__)
            )
        return Counter(
            self.sentence_count + other_inst.sentence_count,
            self.chars_count + other_inst.chars_count,
            self.num_of_words_count + other_inst.num_of_words_count,
            max(self.max_letters_count, other_inst.max_letters_count),
            self.spec_symbols_count + other_inst.spec_symbols_count
        )


class ChunkHandler:
    def __init__(self, chunk: list[str]):
        self.counter = Counter()
        self.chunk = chunk

    def count_sent(self):
        self.counter.sentence_count += 1

    def count_chars_sentence(self, line: str):
        chars = len(line)
        self.counter.chars_count += chars

    def num_of_words_sentence(self, line: str):
        words = len(line.split())
        self.counter.num_of_words_count += words

    def define_max_letters_line(self, line: str):
        letters = len(line.replace(" ", ""))
        if letters > self.counter.max_letters_count:
            self.counter.max_letters_count = letters

    def sentence_with_symbols(self, line, pattern: Pattern[str] = r"[*&^@#%]"):
        if re.search(pattern, line):
            self.counter.spec_symbols_count += 1

    def run_chunk_processing(self):
        for line in self.chunk:
            self.count_sent()
            self.count_chars_sentence(line)
            self.num_of_words_sentence(line)
            self.define_max_letters_line(line)
            self.define_max_letters_line(line)
        return self.counter


def run_chunk_multiprocessing(chunk_handler: ChunkHandler):
    return chunk_handler.run_chunk_processing()
