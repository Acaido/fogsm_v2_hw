from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'https://pokeapi.co/api/v2/'


def by_page(page_size=20, offset=0):
    # В доках к API сказано, что лучше запрашивать постранично,
    # а не все скопом. На каждой странице есть сгенерированная
    # ссылка на следующую страницу или null
    next_page = '{}pokemon/?limit={}&offset={}'.format(
        base_url, page_size, offset
    )
    while next_page:
        request = Request(next_page, headers=headers)
        request = urlopen(request)
        page = request.read()
        page = page.decode()
        page = json.loads(page)
        next_page = page['next']
        for result in page['results']:
            by_id_or_name(result['url'], False)


def by_id_or_name(pokemon, built_url=False):
    if built_url:
        url = pokemon
    else:
        url = '{}pokemon/{}/'.format(base_url, pokemon)

    pokemon_request = Request(url, headers=headers)
    pokemon_request = urlopen(pokemon_request)
    pokemon_data = pokemon_request.read()
    pokemon_data = pokemon_data.decode()
    pokemon_data = json.loads(pokemon_data)
    print('POKEMON: {}'.format(pokemon_data['name'].capitalize()))
    print('\tHeight: {}, weight: {}'.format(
        pokemon_data['height'], pokemon_data['weight']))
    print('Abilities:')
    for ability in pokemon_data['abilities']:
        print('\t{}'.format(ability['ability']['name']))


if __name__ == '__main__':
    print('Введите имя или id покемона.')
    name_or_id = input().lower().strip()
    try:
        by_id_or_name(name_or_id)
    except HTTPError as ex:
        if ex.code == 404:
            print('Покемон с данным именем или '
                  'id {} не найден.'.format(name_or_id))
        else:
            raise
