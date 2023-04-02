import timeit
import cProfile
from main import run_multiprocessing_count, run_single_process_count

FILEPATH = "data/en_GB_BIG.txt"


def timeit_check():
    pass

def timeit_profiling(func: str, repeat: int = 3, number: int = 1):
    """Test func from main.py module"""
    setup = "from main import run_single_process_count, run_multiprocessing_count, run_single_line_count"
    stmt = func + f"('{FILEPATH}')"
    result = timeit.repeat(
        stmt=stmt, repeat=repeat, number=number, setup=setup
    )
    return result

def timeit_profiling_fileservice(func: str, repeat: int = 3, number: int = 1):
    """Test func from file_utils.py module"""
    setup = "from file_utils import FileService, testService"
    stmt = f"FileService('{FILEPATH}')." + func
    result = timeit.repeat(
        stmt=stmt, repeat=repeat, number=number, setup=setup
    )
    return result

def c_profile_profiling(func: str):
    statement = func + f"('{FILEPATH}')"
    cProfile.run(statement)


# print(c_profile_profiling('run_single_process_count'))

print(timeit_profiling('run_single_process_count', number=1))
print(timeit_profiling('run_multiprocessing_count', number=1))
print(timeit_profiling('run_single_line_count', number=1))
# print(timeit_profiling_fileservice('get_count_all_lines()'))
# print(timeit_profiling_fileservice('_count_lines_single_proc()'))


