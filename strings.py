"""
Вариант 1, строки (7).
Определим слова в хэштеге. Дана строка, начинается с # и содержит набор слов,
соединенных в одну строку без пробелов. Срока описана в стиле camelCase,
то есть первое слово начинается с прописной буквы, а каждое следующее с заглавной.
Например: #приветКакДела, #меняЗовутЕгорМнеМногоЛет и тд.
Необходимо посчитать количество слов в строке и вывести количество этих слов.
"""


def parse_hash_str(msg: str) -> int:
    if not msg.startswith('#'):
        raise ValueError("It's not a hash string")
    cnt = 0
    msg = msg.replace('#', '', 1)
    for i, char in enumerate(msg):
        if char.islower() or not char.isalpha():
            if not i == len(msg) - 1:
                continue
        cnt += 1
    return cnt


if __name__ == '__main__':
    m = input()
    print(parse_hash_str(m))
