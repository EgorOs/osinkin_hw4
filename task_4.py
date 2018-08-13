#!/usr/bin/env python3
from time import time, sleep


def parametrized(dec):
    def wrapper(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return wrapper


@parametrized
def make_cache(function, cache_lifetime):
    cache = {}
    cache_by_time = {}

    def wrapper(*args):
        # time_stamps = cache_by_time.keys() # Works for Python 2,
        # but in Py3 cache_by_time.keys() is iterator, not list
        time_stamps = list(cache_by_time)
        for stamp in time_stamps:
            # Clean outdated cache
            if time() - stamp > cache_lifetime:
                key = cache_by_time.pop(stamp)
                cache.pop(key)
        if args in cache:
            return cache[args]
        else:
            val = function(*args)
            cache[args] = val
            cache_by_time[time()] = args
            return val

    return wrapper


@make_cache(2)
def slow_function(n):
    print('No cache for {} yet, go to sleep'.format(n))
    sleep(3)
    return n


init_time = time()
print('Start time', time() - init_time)
for i in range(10):
    t1 = time()
    slow_function(1)
    t2 = time()
    print('Slow function was executed in approximately: {} sec'
          .format(round(t2 - t1), ndigits=3))
    sleep(0.5)
