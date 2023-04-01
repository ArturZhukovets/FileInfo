import multiprocessing
from typing import Generator, Final

from counter import Counter, ChunkHandler, run_chunk_multiprocessing
from file_utils import FileService


def run_single_process_count(file_path: str):
    chunks: Generator = FileService(file_path).get_chunk_by_lines()
    global_values = Counter()

    for chunk in chunks:
        chunk_values: Counter = ChunkHandler(chunk).run_chunk_processing()
        global_values += chunk_values

    return global_values


def run_multiprocessing_count(file_path: str):
    chunks: Generator = FileService(file_path).get_chunk_by_lines()
    pool = multiprocessing.Pool()
    results: Final = pool.map(run_chunk_multiprocessing, map(lambda chunk: ChunkHandler(chunk), chunks))
    global_values = Counter()
    for chunk_value in results:
        global_values += chunk_value

    return global_values


if __name__ == '__main__':
    filepath = "data/big_file.txt"

    single_proc_res = run_single_process_count(filepath)
    multy_proc_res = run_multiprocessing_count(filepath)
    x = 0

