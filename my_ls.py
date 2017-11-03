from os import scandir, fspath, readlink, getcwd
from os.path import join, islink, basename, abspath
import sys


def walk(top, maxdepth=None, tab=''):
    """
    Взял исходник os.walk, вырезал некторый функционал -
    обратный проход и переход по символьным ссылкам на директории.
    Добавил возможность контролировать, на сколько уровней делать
    спуск по дереву каталогов. Параметр tab нужен, чтобы форматировать вывод,
    передавать в него значение не нужно.
    """
    top = fspath(top)
    dirs = []
    nondirs = []

    try:
        scandir_it = scandir(top)
    except OSError:
        return

    for entry in scandir_it:
        # Если не можем получить доступ, считаем файлом.
        try:
            is_dir = entry.is_dir()
        except OSError:
            is_dir = False
        if is_dir:
            dirs.append(entry.name)
        else:
            nondirs.append(entry.name)

    yield top, dirs, nondirs, tab

    if maxdepth is None or maxdepth > 1:
        last = len(dirs) - 1
        for i, dirname in enumerate(dirs):
            new_tab = tab + ('   ' if i == last else '|  ')
            new_path = join(top, dirname)
            if not islink(new_path):
                yield from walk(new_path,
                                maxdepth - 1 if maxdepth else maxdepth, new_tab)


def tree(din, maxdepth=None):
    din = abspath(din)
    for root, dirs, files, tab in walk(din, maxdepth):
        if root == din and din == getcwd():
            print('.')
        else:
            print('{}|- {}'.format(tab[:-3], basename(root)))
        for f in files:
            full_path = join(root, f)
            if islink(full_path):
                out = '{} -> {}'.format(f, readlink(full_path))
            else:
                out = f
            print('{}|- {}'.format(tab, out))


if __name__ == '__main__':
    try:
        tree(sys.argv[1], 2)
    except (FileNotFoundError, NotADirectoryError) as ex:
        print(ex)
    except IndexError:
        print('Передайте путь к директории в качестве первого параметра.')
