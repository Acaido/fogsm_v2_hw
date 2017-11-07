"""
Вариант 7, списки 1.
Дан список чисел. Выведите все элементы списка,
которые больше предыдущего элемента.
"""
import timeit


def clock(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        res = func(*args, **kwargs)
        stop = timeit.default_timer()
        return res, stop - start
    return wrapper


@clock
def print_if_gt_prev(lst):
    # Проверять нулевой элемент нет смысла. Делаем сдвиг и итерируем оба списка
    # со сдвигом и без одновременно. Можно использовать индексы, но на больших
    # списках работать они будут медленнее.
    to_check = lst[1:]
    for prev, cur in zip(lst, to_check):
        if cur > prev:
            print(cur, end=' ')
    print('')


if __name__ == '__main__':
    values = list(map(float, input().split()))
    print_if_gt_prev(values)
