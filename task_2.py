#!/usr/bin/env python3


def mysqrt(x, decimal=0.1, precision=0.001):
    """
    Returns a square root of the integer or float number, if
    resulting float not bigger than sys.float_info.max, which is
    1.7976931348623157e+308

    Parameters:

    decimal   - float, that defines the number of digits after
                decimal point
    precision - float, that defines the error toleration
    """

    def next_guess(x, guess, precision=0.001):
        new_guess = (guess + x / guess) / 2
        error = abs(new_guess - guess)
        if error < precision:
            return new_guess
        else:
            return next_guess(x, new_guess, precision)

    if x < 0: raise ValueError('{} is not positive number'.format(x))
    if x == 0: return 0
    if x == 1: return 1
    
    decimal_str = str(decimal)
    if 'e' in decimal_str:
        # for representation like 1e-11
        decimal = int(decimal_str.split('-')[1])
    else:
        decimal = len(decimal_str.split('.')[1])
    return round(next_guess(x, x // 2, precision), ndigits=decimal)


# print(mysqrt(5, 0.01))
