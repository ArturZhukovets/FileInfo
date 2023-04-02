import itertools
import multiprocessing
import os
import subprocess
from typing import Generator

def count_lines_in_chunk(chunk):
    return chunk.count('\n')


class FileService:

    CHUNK_SIZE_LINES: int = 1000

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.count_lines = self.get_count_all_lines()

    def readline(self):
        with open(self.filepath, 'r', encoding='utf-8') as f_o:
            for line in f_o:
                yield line

    def readline_mmap(self):
        # TODO TRY TO USE MMAP
        pass

    def num_chunks(self) -> int:
        num_chunks = self.count_lines // self.CHUNK_SIZE_LINES
        if num_chunks % self.CHUNK_SIZE_LINES != 0:
            num_chunks += 1
        return num_chunks

    def get_count_all_lines(self) -> int:
        completed_process = subprocess.run(['wc', '-l', self.filepath], capture_output=True, text=True)
        output = completed_process.stdout.strip()
        return int(output.split()[0])

    def get_size(self):
        return os.path.getsize(self.filepath) / (1024 * 1024)

    def get_chunk_of_lines(self) -> Generator[list[str], None, None]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            while True:
                batch = list(itertools.islice(f, self.CHUNK_SIZE_LINES))
                if not batch:
                    break
                yield batch

    def _count_lines_single_proc(self) -> int:
        counter = 0
        for _ in self.readline():
            counter += 1
        return counter


# ======================================== Testing |

testService = FileService("data/en_GB_BIG.txt")
# print(testService.get_count_all_lines())
# print(testService._count_lines_single_proc())

