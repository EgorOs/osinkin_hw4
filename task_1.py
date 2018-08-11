#!/usr/bin/env python3
import sys


class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.
    This function fails if the decorated
    function recurses in a non-tail context.
    """

    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back \
                and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


@tail_call_optimized
def str_to_int(content: str, acc=0) -> int:
    if content:
        ch, content = content[0], content[1:]
    else:
        return acc
    if ch.isdigit():
        return str_to_int(content, acc * 10 + int(ch))
    else:
        print('Could not convert str to int, sting contains non-digit symbols')


# print(str_to_int('1337'*1000)) # tail call optimization test
while True:
    usr_input = input("Type anything...\n>>> ")
    if usr_input == "cancel":
        break
    else:
        num = str_to_int(usr_input)
        if num:
            if num % 2 == 0:
                print(num // 2)
            else:
                print(num * 3 + 1)
