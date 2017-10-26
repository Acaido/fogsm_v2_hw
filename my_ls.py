import os
import sys


def print_entries(din):
    for entry in sorted(os.listdir(din)):
        print(entry)


if __name__ == '__main__':
    try:
        print_entries(sys.argv[1])
    except (FileNotFoundError, NotADirectoryError) as ex:
        print(ex)
    except IndexError:
        print('Передайте путь к директории в качестве первого параметра.')
