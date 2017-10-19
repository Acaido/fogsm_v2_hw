"""
Вариант 7, списки 1.
Дан список чисел. Выведите все элементы списка, которые больше предыдущего элемента.
"""


def print_gt_prev(lst):
    # todo: два вложенных списка не надо, можно сделать проще.
    for i, item in enumerate(lst):
        print([x for x in lst if i > 0 and x > lst[i - 1]])


if __name__ == '__main__':
    lst_in = list(map(float, input().split()))
    print_gt_prev(lst_in)

