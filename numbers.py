"""
Вариант 1, числа (1).
Дано комплексное число  Z, вида Z=x+jy,
где x и y - вещественные числа, а j - мнимая единица.
Необходимо представить данное число в полярной системе координат,
которое определяется r - длинной вектора z,
и phi - углом поворота вектора Z против часовой стрелки.
"""
# import math
import cmath


def c_rect2pol(cnum: complex) -> tuple:
    """
    :param cnum: complex number in rectangular coordinates
    :return: tuple consists of absolute value and argument of complex number
    in radians
    """
    # return (math.sqrt(cnum.real ** 2 + cnum.imag ** 2),
    #         math.atan2(cnum.imag, cnum.real))

    return cmath.polar(cnum)


if __name__ == '__main__':
    # z = 10 + 3j
    # print(c_rect2pol(z))  # (10.44030650891055, 0.2914567944778671)
    z = input()
    print(c_rect2pol(complex(z.replace(' ', ''))))
