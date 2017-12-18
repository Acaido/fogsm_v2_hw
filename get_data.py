import urllib.request as ur
from hparse import PageLinks
import json
import psycopg2
import configparser


config = configparser.ConfigParser()
config.read('conf.ini')
conn = psycopg2.connect(config['database']['connection'])

langs = {}
with conn.cursor() as cur:
    cur.execute('select name, id from public.languages;')
    for lang, lang_id in cur.fetchall():
        langs[lang] = lang_id

headers = {
    'User-Agent': 'Acaido',
    'Accept': 'application/vnd.github.mercy-preview+json'
}

charset = 'utf-8'
user_query = 'INSERT INTO public.users VALUES (%s, %s) ON CONFLICT DO NOTHING'
repo_query = ('INSERT INTO public.repositories '
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
              'ON CONFLICT DO NOTHING')
lang_query = ('INSERT INTO public.lang_repo '
              'VALUES (%s, %s) ON CONFLICT DO NOTHING')
insert_lang_query = ('INSERT into public.languages (name) VALUES (%s)'
                     'RETURNING id')

next_page = 'https://api.github.com/users'
try:
    while next_page is not None:
        request = ur.Request(next_page, headers=headers)
        response = ur.urlopen(request)

        users = response.read().decode(charset)
        users = json.loads(users)
        for user in users:
            with conn.cursor() as cur:
                cur.execute(user_query, (user['id'], user['login']))
                conn.commit()

            repo_req = ur.Request(user['repos_url'], headers=headers)
            repo_resp = ur.urlopen(repo_req)
            repos = repo_resp.read().decode(charset)
            repos = json.loads(repos)
            for repo in repos:
                lang_req = ur.Request(repo['languages_url'], headers=headers)
                lang_resp = ur.urlopen(lang_req)
                languages = lang_resp.read().decode(charset)
                languages = json.loads(languages)
                if not len(languages):
                    languages = {None: ''}
                with conn.cursor() as cur:
                    cur.execute(repo_query,
                                (repo['id'], repo['name'], repo['html_url'],
                                 repo['created_at'], repo['updated_at'],
                                 repo['pushed_at'], repo['stargazers_count'],
                                 repo['forks'], user['id']))
                    for lang in languages.keys():
                        if lang not in langs.keys():
                            cur.execute(insert_lang_query, (lang,))
                            id_ = cur.fetchone()[0]
                            langs[lang] = id_
                        cur.execute(lang_query, (langs[lang], repo['id']))
                conn.commit()
        plinks = PageLinks(response)
        next_page = plinks.next

        life = 'is good'
except ur.HTTPError as ex:
    print(ex)