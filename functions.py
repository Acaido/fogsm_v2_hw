"""
Вариант 7, функции 7.
Реализовать функцию map, принимающей два аргумента: список и произвольную арифметическую функцию.
Функция map должна возвращать новый список, элементы которого являются результатом функции func.

Например
Определим функцию func(x), которая возвращает квадрат аргумента:
>>> def func(x):
>>>     return x**2
>>>
Где-то выше определили функцию map и передали ей список и ссылку на функцию:
>>> map([1, 2, 3], func)
В результате получаем:
>>> [1, 4, 9]
"""
import random
import math


def square(x):
    return x ** 2


def my_map(it, func):
    return [func(i) for i in it]


if __name__ == '__main__':
    functions = [square, math.sqrt, math.exp, math.log]
    lst = list(map(float, input().split()))
    samples = random.sample(functions, random.randint(1, len(functions)))
    for f in samples:
        print(f, my_map(lst, f), sep='\n')