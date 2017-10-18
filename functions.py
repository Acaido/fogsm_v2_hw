"""
Вариант 1, функции (1).
Даны четыре действительных числа: x1, y1, x2, y2.
Напишите функцию distance(x1, y1, x2, y2),
вычисляющая расстояние между точкой (x1,y1) и (x2,y2).
Считайте четыре действительных числа и выведите результат работы этой функции.
"""
from math import sqrt


def distance(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    args = input().split()
    if len(args) != 4:
        raise ValueError('4 numbers suspected. Given {} instead.'.format(len(args)))
    args = list(map(float, args))
    print(distance(*args))
