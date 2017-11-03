import sys


class WrongScheduleError(Exception):
    pass


WEEK_DAYS = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')


def main(fin):
    # Ключи соответсвуют типам занятий в файле-расписании.
    counter = {
        'лекция': 0,
        'практика': 0,
        'лабораторная': 0
    }
    keys = counter.keys()
    try:
        with open(fin, 'r') as fi:
            for line in fi:
                striped = line.strip()
                capitalized = striped.capitalize()
                if capitalized in WEEK_DAYS or striped == '':
                    continue
                if capitalized == 'Воскресенье':
                    raise WrongScheduleError(
                        'Это какое-то неправильное расписание. Делали его неправильные люди.')
                try:
                    # Тип занятия значится в конце строки в скобках, например
                    # (лекция) или (практика). Сначала разделяем строку левой
                    # скобкой по первому вхождению и берем все, что справа -
                    # split('(', 1)[1] -> "лекция)...", затем остаток разделяем
                    # правой скобкой также по первому вхождению и берем все,
                    # что слева - split(')', 1)[0] -> "лекция".
                    occupation_type = striped.split('(', 1)[1].split(')', 1)[0]
                except IndexError:
                    print(
                        'Бардак в расписании. Что это - "{}"?'.format(striped))
                    continue
                if occupation_type in keys:
                    counter[occupation_type] += 1
        print('ИТОГО:', counter)
    except FileNotFoundError:
        print('Given file {} is not found.'.format(fin))


if __name__ == '__main__':
    try:
        schedule = sys.argv[1]
    except IndexError:
        print('Введите путь к файлу с расписанием.')
        schedule = input()
    try:
        main(schedule)
    except WrongScheduleError as ex:
        print('{} Создайте человеческие условия!'.format(ex))
