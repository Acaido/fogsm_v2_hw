"""
Вариант 1, числа (1).
Дано комплексное число  Z, вида Z=x+jy,
где x и y - вещественные числа, а j - мнимая единица.
Необходимо представить данное число в полярной системе координат,
которое определяется r - длинной вектора z,
и phi - углом поворота вектора Z против часовой стрелки.
"""
import cmath


def c_rect2pol(cnum: complex) -> tuple:
    """
    :param cnum: complex number in rectangular coordinates
    :return: tuple consists of absolute value and argument of complex number
    in radians
    """
    return cmath.polar(cnum)


if __name__ == '__main__':
    z = input()
    print(c_rect2pol(complex(z.replace(' ', ''))))
