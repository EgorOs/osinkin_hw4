#!/usr/bin/env python3
from time import time, sleep
import math


def parametrized(dec):
    def wrapper(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return wrapper


@parametrized
def profiler(function, calls_info):
    def wrapper(*args, **kwargs):
        start_time = time()*1000
        result = function(*args, **kwargs)
        end_time = time()*1000
        execution_time = end_time - start_time

        if globals().get(calls_info):
            ctr, t = globals()[calls_info]
            globals()[calls_info] = (ctr + 1, t + execution_time)
        else:
            globals()[calls_info] = (1, execution_time)
        return result

    return wrapper


@profiler('test_gold')
def golden_ratio( n ):
    phi = (1 + math.sqrt( 5 ) ) / 2
    psi = (1 - math.sqrt( 5 ) ) / 2
    return round(( phi**n ) / math.sqrt( 5 ))


@profiler('test_rec')
def fib_rec(n):
    if n < 3:
        return 1
    else:
        return fib_rec(n - 1) + fib_rec(n - 2)


@profiler('test_iter')
def fib_iter(n):
    a = 0
    b = 1
    for __ in range(n):
        a, b = b, a + b
    return a


@profiler('test_marix')
def fib_matrix(n):
    def my_pow(x, k, I, mult):
        """
        Возвращает x в степени n. Предполагает, что I – это единичная матрица, которая
        перемножается с mult, а n – положительное целое
        """
        if k == 0:
            return I
        elif k == 1:
            return x
        else:
            y = my_pow(x, k // 2, I, mult)
            y = mult(y, y)
            if k % 2:
                y = mult(x, y)
            return y

    def identity_matrix(j):
        """Возвращает единичную матрицу n на n"""
        r = list(range(j))
        return [[1 if i == j else 0 for i in r] for j in r]

    def matrix_multiply(A, B):
        bt = list(zip(*B))
        return [[
            sum(a * b for a, b in zip(row_a, col_b))
            for col_b in bt]
            for row_a in A]
    f = my_pow([[1, 1], [1, 0]], n, identity_matrix(2), matrix_multiply)
    return f[0][1]


n = 30

print(fib_rec(n))
print('Recursive\ncalls: {}\ntime(ms): {}'.format(*test_rec))
print(fib_iter(n))
print('Iterative\ncalls: {}\ntime(ms): {}'.format(*test_iter))
print(fib_matrix(n))
print('Matirx\ncalls: {}\ntime(ms): {}'.format(*test_marix))
print(golden_ratio(n))
print('Gold ratio\ncalls: {}\ntime(ms): {}'.format(*test_gold))
