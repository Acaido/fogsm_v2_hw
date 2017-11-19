"""
4. Создать абстрактный класс Figure с методами вычисления площади и периметра,
а также методом, выводящим информацию о фигуре на экран. Создать производные
классы: Rectangle (прямоугольник), Circle (круг), Triangle (треугольник) со
своими методами вычисления площади и периметра. Создать массив n фигур и
вывести полную информацию о фигурах на экран.
"""
from abc import ABCMeta, abstractmethod
from math import pi, sqrt


class Figure(metaclass=ABCMeta):
    @abstractmethod
    def perimeter(self):
        pass

    @abstractmethod
    def area(self):
        pass

    def __str__(self):
        return 'Hello, I\'m a {} with perimeter={:.2f} and area={:.2f}.'.format(
            self.__class__.__name__, self.perimeter(), self.area())

    def __repr__(self):
        return str(self)


class Rectangle(Figure):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def perimeter(self):
        return (self.width + self.height) * 2

    def area(self):
        return self.width * self.height

    def __str__(self):
        return '{} My params: width={}, height={}'.format(
            super().__str__(), self.width, self.height)


class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius

    def perimeter(self):
        return 2 * pi * self.radius

    def area(self):
        return pi * self.radius * self.radius

    def __str__(self):
        return '{} My radius={}'.format(super().__str__(), self.radius)


class Triangle(Figure):
    def __init__(self, a, b, c):
        # Проверим, чтобы длины сторон (достаточно проверить наибольшую)
        # не превышали и не были равны сумме длин двух других.
        sides = (a, b, c)
        for side in sides:
            other_sides_sum = sum(sides) - side
            if side >= other_sides_sum:
                raise ValueError(
                    'Длина стороны {}  превышает сумму {} двух других '
                    'или равна ей.'.format(side, other_sides_sum))
        self.a = a
        self.b = b
        self.c = c

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        # Используем формулу Герона.
        s = self.perimeter() / 2.
        return sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def __str__(self):
        return '{} My sides: a={}, b={}, c={}'.format(
            super().__str__(), self.a, self.b, self.c)


if __name__ == '__main__':
    import random

    # Сгенерируем 'number' фигур с параметрами, значения которых лежат в
    # диапазоне от 'lower' до 'upper'.
    number = 7
    lower = 1
    upper = 9
    # Фигуры имеют разное количесво параметров. Будем хранить в словарике,
    # чтобы знать сколько их генерировать под каждую фигуру.
    available_figures = {
        Circle: 1,
        Rectangle: 2,
        Triangle: 3
    }
    figures = random.choices(list(available_figures.keys()), k=number)
    for figure in figures:
        params = [random.uniform(lower, upper) for _ in range(
            available_figures[figure])]
        # На случай, если сгенерируется "кривой" треуголник.
        try:
            fig = figure(*params)
            print(fig)
        except ValueError as ex:
            print(ex)
