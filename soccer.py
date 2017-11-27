from urllib.request import urlopen
from urllib.error import HTTPError
import json
import random


def key_function(obj):
    return obj['goals']


request = urlopen('http://api.football-data.org/v1/competitions/')
tournaments = request.read()
tournaments = tournaments.decode()
tournaments = json.loads(tournaments)
# Не придумал критерий популярности чемпионатов. Поэтому просто 5 случайных.
tournaments = random.choices(tournaments, k=5)
for tournament in tournaments:
    league_url = tournament['_links']['leagueTable']['href']
    try:
        tour_request = urlopen(league_url)
    except HTTPError as ex:
        if ex.code == 404:
            print('Битая ссылка\n\t{}'.format(league_url))
            continue
        elif ex.code == 403:
            # По некоторым ссылкам требует авторизацию, например тут -
            # http://api.football-data.org/v1/competitions/466
            # Соотвественно, при запросе инфы по лиге возникает access denied -
            # http://api.football-data.org/v1/competitions/466/leagueTable
            print('Нет доступа\n\t{}.'.format(league_url))
            continue
        raise
    league = tour_request.read()
    league = league.decode()
    league = json.loads(league)

    # Команды содержатся под одним ключом или разбиты в группы по 4.
    if 'standing' in league.keys():
        teams = league['standing']
        team_name_key = 'teamName'
    else:
        # Команды разбиты в группы по 4. Выберем с наибольшим количеством голов
        # в каждой группе, затем топ-5.
        teams = []
        for _, group in league['standings'].items():
            teams.append(max(group, key=key_function))
        team_name_key = 'team'

    teams = sorted(teams, key=key_function, reverse=True)
    print('LEAGUE "{}"'.format(league['leagueCaption']))
    for team in teams[0:5]:
        print('\tTeam "{}", goals: {}'.format(
            team[team_name_key], team['goals']))
