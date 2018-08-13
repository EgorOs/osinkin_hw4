#!/usr/bin/env python3
from time import time, sleep


def parametrized(dec):
    def wrapper(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return wrapper


@parametrized
def profiler(function, calls_info):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = function(*args, **kwargs)
        end_time = time()
        execution_time = end_time - start_time

        if globals().get(calls_info):
            ctr, t = globals()[calls_info]
            globals()[calls_info] = (ctr + 1, t + execution_time)
        else:
            globals()[calls_info] = (1, execution_time)
        return result

    return wrapper


# Factorial 1
class Recurse(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def recurse(*args, **kwargs):
    raise Recurse(*args, **kwargs)


def tail_recursive(f):
    def decorated(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Recurse as r:
                args = r.args
                kwargs = r.kwargs
                continue

    return decorated


@profiler('F1_info')
@tail_recursive
def fact(n, acc=1):
    if n == 1: return acc
    return recurse(n - 1, n * acc)


# Factorial 2
@profiler('F2_info')
def factorial(n):
    if n < 0:
        return
    if n == 0:
        return 1
    return n * factorial(n - 1)


# Factorial 3
@profiler('F3_info')
def tail_factorial(n, acc=1):
    if n < 0:
        return
    if n == 1:
        return acc
    return tail_factorial(n - 1, acc * n)


n = 200
print('\nFactorial of', n)
print('\nTail_recursive with decorator:')
print(fact(n))
print('Calls: {}, total time: {}'.format(*F1_info))

print('\nUnoptimized:')
print(factorial(n))
print('Calls: {}, total time: {}'.format(*F2_info))

print('\nTail call optimization:')
print(tail_factorial(n))
print('Calls: {}, total time: {}'.format(*F3_info))
