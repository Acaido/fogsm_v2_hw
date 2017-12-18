from datetime import datetime
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')
conn = psycopg2.connect(config['database']['connection'])


# 1. Получим список статей/репозиториев по заданному хэш-тэгу
# в заданный период времени;
def from_to_by_language(lang, date_start, date_end):
    with conn.cursor() as cur:
        cur.execute(
            'SELECT r.name, r.link, r.updated, r.stars, r.forks, '
            'u.login as owner_name, l.name '
            'FROM repositories r '
                'INNER JOIN users u on r.owner = u.id '
                'INNER JOIN lang_repo lr on r.id=lr.repo_id '
                'INNER JOIN languages l on lr.lang_id = l.id '
            'WHERE lower(l.name) = %s '
            'AND r.updated BETWEEN %s and %s ',
            (lang.lower().strip(), date_start, date_end))
        for row in cur:
            print(row)
    conn.commit()


# 2. Получаем список популярных статей/репозиториев за неделю;
def top_five_repos_for_week():
    # Даты смотрим по последнему обновлению в репозитории.
    # Сначала смотрим у кого больше звездочек, потом отпочкованных проектов.
    query = ('SELECT id, name, link, updated, stars, forks FROM repositories '
             "WHERE updated > now() at TIME ZONE 'UTC' + '-1 week'"
             'ORDER BY stars DESC, forks DESC '
             'LIMIT 5')
    with conn.cursor() as cur:
        cur.execute(query)
        for row in cur.fetchall():
            print(row)
    conn.commit()


# 3. Получаем топ 10 популярных хэш-тэгов, т.е. те,
# у которых больше всего статей/репозиториев;
# // С хэштегами возникла проблема - всегда пустой список. Функция пока
# экспериментальная, но согласно докам, можно ей пользоваться указав
# в хидере 'Accept': 'application/vnd.github.mercy-preview+json'. Но что-то не
# помогло. Поэтому теги заменил на языки.
def top_ten_languages():
    query = ('SELECT name, count(repo_id) AS repo_cnt '
             'FROM languages '
             'INNER JOIN lang_repo ON languages.id = lang_repo.lang_id '
             'GROUP BY name '
             'ORDER BY repo_cnt DESC '
             'LIMIT 10 ')
    with conn.cursor() as cur:
        cur.execute(query)
        print('{:<20}\t{}'.format('language', 'repos count'))
        for row in cur.fetchall():
            lang, cnt = row
            if lang is None:
                lang = '<null>'
            print('{:<20}\t{:>3}'.format(lang, cnt))
    conn.commit()


# 4. Получаем список самых активных пользователей,
# те, у которых больше всего статей. //  В данном случае репозиториев.
def top_five_active_users():
    query = ('SELECT u.login AS user_name, count(r.name) AS repo_cnt '
             'FROM github.public.repositories r '
             'INNER JOIN github.public.users u ON u.id=r.owner '
             'GROUP BY user_name '
             'ORDER BY repo_cnt DESC '
             'LIMIT 5 ')
    with conn.cursor() as cur:
        cur.execute(query)
        print('{:<20}\t{}'.format('user', 'repos count'))
        for row in cur.fetchall():
            print('{:<20}\t{:>3}'.format(*row))
    conn.commit()


from_to_by_language('Python', datetime(2017,1,1), datetime.utcnow())
print('')
top_five_repos_for_week()
print('')
top_ten_languages()
print('')
top_five_active_users()
