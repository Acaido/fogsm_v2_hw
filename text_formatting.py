"""
7. Дан файл с текстом. Написать скрипт, который форматирует текст к следующему
стилю:
1) Название файла выводится в самом начале текста, центруется и выводится
заглавными буквами.
2) Весь текст выравнивается по центру.
3) Каждый абзац разделен пустой строкой.
4) Начало каждого абзаца содержит отступ от левого края в 4 пробела и начинается
с большой буквы.
5) В конце документа имя и фамилия автора.
"""
from os.path import basename, splitext
import argparse


def main(file_to_format, max_width=80, author='Anonymous'):
    if max_width < 0:
        raise ValueError(
            'Максимальная ширина строки должна быть положительным числом. '
            'Получено: {}'.format(max_width)
        )
    # Создаем форматтер для выравнивания строк по центру - '^' ('<' - по левому
    # краю, '>' - по правому), задаем ширину строки, без которой выравнивание
    # не сработает, т.к. по-умолчанию ширина определяется на основе содержимого.
    formatter = '{:^' + str(max_width) + '}\n'
    with open(file_to_format) as fin, open(
            '{}.formatted{}'.format(*splitext(file_to_format)), 'w') as fout:
        # Получаем имя файла из абсолютного пути, выводим его заглавными буквами
        # первой строкой по центру, используя форматтер.
        header = basename(fin.name)
        header = header.upper()
        fout.write(formatter.format(header))
        for line in fin:
            # Пустые строки пропускаем.
            if line.strip() == '':
                continue
            # Абзацы разеделены пустой строкой.
            fout.write('\n')
            # Форматтер не переносит текст на новую строку, если тот превышает
            # заданную длину, поэтому необходимо позаботиться об этом
            # самостоятельно.
            words = line.split()
            words = iter(words)
            # Первая строка в абзаце начинается с красной строки в 4 пробела и с
            # заглавной буквы. Пустные строки пропускаются, поэтому хотя бы одно
            # слово будет. Значит IndexError при выполнении next() не словим.
            to_print = '    ' + next(words).capitalize()
            for word in words:
                word = ' ' + word
                if len(to_print + word) < max_width:
                    to_print = to_print + word
                else:
                    fout.write(formatter.format(to_print))
                    to_print = word
            # Слова в абзаце кончились,
            # а неполная строка еще не записана в файл.
            if len(to_print):
                fout.write(formatter.format(to_print))
        fout.write('\n')
        fout.write(formatter.format(author))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'file_to_format',
        help='Файл, содержимое которого будет отформатированно '
             'и записано в другой файл.'
    )
    parser.add_argument(
        '-w', '--max_width', default=80, type=int,
        help='Максимальная длина строки в форматированном тексте.'
    )
    parser.add_argument(
        '-a', '--author', default='Anonymous',
        help=('Имя автора. Будет добавлено в конце форматированного текста.'
              'Имя, разделенное пробелами, необходимо брать в кавычки')
    )
    args = parser.parse_args()
    try:
        main(args.file_to_format, args.max_width, args.author)
    except (FileNotFoundError, OSError, ValueError) as ex:
        print(ex)
