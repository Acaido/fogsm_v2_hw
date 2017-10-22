"""
Вариант 7, списки 1.
Дан список чисел. Выведите все элементы списка, которые больше предыдущего элемента.
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
def print_gt_prev(lst):
    for i, item in enumerate(lst):
        if i == 0:
            continue
        print([x for x in lst if x > lst[i - 1]])


@clock
def print_gt_prev_1(lst):
    s = sorted(lst)
    for item in lst[:-1]:
        i = s.index(item)
        print(s[i+1:])


if __name__ == '__main__':
    values = list(map(float, input().split()))
    print('values: ', values)
    _, time = print_gt_prev(values)
    print(time)
    _, time_1 = print_gt_prev_1(values)
    print(time_1)
    print('time > time_1', time > time_1, abs(time-time_1))