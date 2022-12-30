""" Elapsed time counter. """
from colored import fg, attr
import time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, *kwargs)
        elapsed = time.perf_counter() - start
        print(f"{fg('#444')}Время обработки: {elapsed:.3f} сек.{attr('reset')}")

    return wrapper
