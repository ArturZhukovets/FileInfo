import time
import timeit

def timeit_check():
    pass


filepath = "data/en_GB_BIG.txt"

res_time_single_proc = timeit.repeat(
    stmt=f"run_single_process_count('{filepath}')", repeat=3, number=1,
    setup="from main import run_single_process_count"
)

res_time_multy_proc = timeit.repeat(
    stmt=f"run_multiprocessing_count('{filepath}')", repeat=3, number=1,
    setup="from main import run_multiprocessing_count"
)


print(res_time_single_proc)
print(res_time_multy_proc)


