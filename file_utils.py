import itertools
import os
from typing import Generator

from counter import ChunkHandler


class FileService:

    CHUNK_SIZE_LINES: int = 10

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.number_of_lines = None

    def readline(self):
        with open(self.filepath, 'r', encoding='utf-8') as f_o:
            for line in f_o:
                yield line

    @staticmethod
    def readline_chunk(chunk: list[str]):
        for line in chunk:
            yield line

    def readline_mmap(self):
        # TODO TRY TO USE MMAP
        pass

    def count_lines(self):
        counter = 0
        for _ in self.readline():
            counter += 1
        self.number_of_lines = counter
        return counter

    def get_size(self):
        return os.path.getsize(self.filepath) / (1024 * 1024)

    def _num_chunks(self) -> int:
        num_chunks = self.count_lines() // self.CHUNK_SIZE_LINES
        if num_chunks % self.CHUNK_SIZE_LINES != 0:
            num_chunks += 1
        return num_chunks

    def get_chunk_by_lines(self) -> Generator[list[str], None, None]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            while True:
                batch = list(itertools.islice(f, self.CHUNK_SIZE_LINES))
                if not batch:
                    break
                yield batch
