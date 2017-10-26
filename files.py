import sys


class WrongScheduleError(Exception):
    """"""


WEEK_DAYS = 'понедельник вторник среда четверг пятница суббота'.split()


def main(fin):
    counter = {
        'лекц.': 0,
        'практ.': 0,
        'лаб.': 0
    }
    keys = counter.keys()
    try:
        with open(fin, 'r') as fi:
            for line in fi:
                striped = line.strip()
                if striped.lower() in WEEK_DAYS or striped == '':
                    continue
                if striped.lower() == 'воскресенье':
                    raise WrongScheduleError(
                        'Это какое-то неправильное расписание. Делали его неправильные люди.')
                try:
                    occupation_type = striped.split('(', 1)[1].split(')', 1)[0]
                except IndexError:
                    print('Бардак в расписании. Что это - "{}"?'.format(striped))
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
