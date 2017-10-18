"""
Варинат 1, списки (7).
Даны два списка произвольной длины каждый.
Списки могут содержать как числа, так и строки.
Необходимо вывести только те элементы, которые входят как первый список, так и во второй.
"""


def inner_join(left, right):
    return list(set(left) & set(right))


if __name__ == '__main__':
    a = [x for x in input().split()]
    b = [x for x in input().split()]
    print(inner_join(a, b))
