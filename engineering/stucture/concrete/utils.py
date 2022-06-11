# -*- encoding=utf-8 -*-

from math import sqrt
from typing import Callable


def log(func: Callable):
    def wrapper(**kwargs):
        print(func.__name__, kwargs)
        return func(**kwargs)

    return wrapper


class NotDefinedByStandard(BaseException):
    def __init__(self, *args):
        self.args = args

class DesignFailure(BaseException):
    def __init__(self, *args):
        self.args = args


def get_α1_and_β1(fcu: float | int):
    if fcu <= 50:
        return 1.0, 0.8
    elif 50 < fcu <= 80:
        return 1.0 - (fcu - 50) * (1.0 - 0.94) / (80 - 50), 0.8 - (fcu - 50) * (
            0.80 - 0.74
        ) / (80 - 50)
    else:
        raise NotDefinedByStandard("C{fcu}'s α1")


def get_ξb(β1: float, fy: float, Es: float, εcu: float):
    return β1 / (1 + fy / Es / εcu)


def get_root(A: float, B: float, C: float):
    Δ = B ** 2 - 4 * A * C
    return (-B - sqrt(Δ)) / (2 * A), (-B + sqrt(Δ)) / (2 * A)


def get_ρmin(ft: float, fy: float):
    return 0.45 * ft / fy


def get_larger_root(A: float, B: float, C: float):
    __smaller, __larger = get_root(A, B, C)
    return __larger


C20 = {"fcu": 20, "fc": 9.6, "ft": 1.1, "Ec": 2.55e4}
C25 = {"fcu": 25, "fc": 11.9, "ft": 1.27, "Ec": 2.55e4}
C30 = {"fcu": 30, "fc": 14.3, "ft": 1.43, "Ec": 2.55e4}

Q300 = {"dmin": 6, "dmax": 22, "fy": 270, "Es": 2.1e5}
Q335 = {"dmin": 6, "dmax": 50, "fy": 300, "Es": 2.0e5}
Q400 = {"dmin": 6, "dmax": 50, "fy": 360, "Es": 2.0e5}
Q500 = {"dmin": 6, "dmax": 50, "fy": 435, "Es": 2.0e5}
