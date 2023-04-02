import multiprocessing
from typing import Generator, Final
from tqdm import tqdm
from counter import Counter, ChunkHandler, run_chunk_multiprocessing, LineHandler
from file_utils import FileService

def run_single_line_count(file_path: str):
    res = Counter()
    for line in FileService(file_path).readline():
        res += LineHandler(line).run_line_processing()
    return res

def run_single_process_count(file_path: str):
    chunks: Generator = FileService(file_path).get_chunk_of_lines()
    global_values = Counter()

    for chunk in chunks:
        chunk_values: Counter = ChunkHandler(chunk).run_chunk_processing_default()
        global_values += chunk_values

    return global_values


def run_multiprocessing_count(file_path: str):
    chunks: Generator = FileService(file_path).get_chunk_of_lines()
    num_chunks = FileService(file_path).num_chunks()

    with multiprocessing.Pool() as pool, tqdm(total=num_chunks, unit='chunks') as progress_bar:
        results: Final = pool.imap(run_chunk_multiprocessing, map(lambda chunk: ChunkHandler(chunk), chunks))
        global_values = Counter()
        for chunk_value in results:
            global_values += chunk_value
            progress_bar.update()
    return global_values


if __name__ == '__main__':
    filepath = "data/en_GB_BIG.txt"

    # single_proc_res = run_single_process_count(filepath)
    # print(single_proc_res)
    multy_proc_res = run_multiprocessing_count(filepath)
    print(multy_proc_res)


    single_line_handler = run_single_line_count(filepath)
    print(single_line_handler)



