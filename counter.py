import re
from dataclasses import dataclass
from typing import Pattern

PARAMETERS_NEED_TO_EVALUATE = [
    'num_of_words_sentence',
    'count_chars_sentence',
    'define_max_letters_line',
    'sentence_with_symbols',
]

@dataclass
class Counter:
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
            self.chars_count + other_inst.chars_count,
            self.num_of_words_count + other_inst.num_of_words_count,
            max(self.max_letters_count, other_inst.max_letters_count),
            self.spec_symbols_count + other_inst.spec_symbols_count
        )


class ChunkHandler:
    def __init__(self, chunk: list[str]):
        self.counter = Counter()
        self.chunk = chunk
        self.all_parameters = {
            'count_chars_sentence': self.count_chars_sentence,
            'num_of_words_sentence': self.num_of_words_sentence,
            'define_max_letters_line': self.define_max_letters_line,
            'sentence_with_symbols': self.sentence_with_symbols,
        }

    def count_chars_sentence(self, line: str) -> None:
        chars = len(line)
        self.counter.chars_count += chars

    def num_of_words_sentence(self, line: str) -> None:
        words = len(line.split())
        self.counter.num_of_words_count += words

    def define_max_letters_line(self, line: str) -> None:
        letters = len(line.replace(" ", ""))
        if letters > self.counter.max_letters_count:
            self.counter.max_letters_count = letters

    def sentence_with_symbols(self, line, pattern: Pattern[str] = r"[*&^@#%]") -> None:
        if re.search(pattern, line):
            self.counter.spec_symbols_count += 1

    def run_chunk_processing(self) -> Counter:
        """If you need to calculate certain parameters."""
        for line in self.chunk:
            for param in PARAMETERS_NEED_TO_EVALUATE:
                if param in self.all_parameters:
                    self.all_parameters[param](line)
        return self.counter

    def run_chunk_processing_getattr(self) -> Counter:
        """If needed to calculate certain parameters use getattr()."""
        for line in self.chunk:
            for param in PARAMETERS_NEED_TO_EVALUATE:
                func = getattr(ChunkHandler, param, None)
                if func:
                    func(self, line)
        return self.counter

    def run_chunk_processing_default(self) -> Counter:
        """If needed to calculate all parameters"""
        for line in self.chunk:
            self.count_chars_sentence(line)
            self.num_of_words_sentence(line)
            self.define_max_letters_line(line)
            self.define_max_letters_line(line)
        return self.counter


class LineHandler:
    def __init__(self, line: [str]):
        self.counter = Counter()
        self.line = line

    def count_chars_sentence(self) -> None:
        chars = len(self.line)
        self.counter.chars_count += chars

    def num_of_words_sentence(self) -> None:
        words = len(self.line.split())
        self.counter.num_of_words_count += words

    def define_max_letters_line(self) -> None:
        letters = len(self.line.replace(" ", ""))
        if letters > self.counter.max_letters_count:
            self.counter.max_letters_count = letters

    def sentence_with_symbols(self, pattern: Pattern[str] = r"[*&^@#%]") -> None:
        if re.search(pattern, self.line):
            self.counter.spec_symbols_count += 1

    def run_line_processing(self) -> Counter:
        self.count_chars_sentence()
        self.num_of_words_sentence()
        self.define_max_letters_line()
        self.sentence_with_symbols()
        return self.counter


def run_chunk_multiprocessing(chunk_handler: ChunkHandler):
    return chunk_handler.run_chunk_processing()
