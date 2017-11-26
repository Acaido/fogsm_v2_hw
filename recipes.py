from urllib.request import urlopen
from urllib.parse import urlencode
import json


def get_recipes(ingredients):
    if not isinstance(ingredients, str) and hasattr(ingredients, '__iter__'):
        ingredients = ','.join(ingredients)

    params = urlencode({'i': ingredients})
    url = 'http://www.recipepuppy.com/api/'
    url = '{}?{}'.format(url, params)

    request = urlopen(url)
    data = request.read()
    data = json.loads(data, encoding='utf-8')
    recipes = data['results']
    for recipe in recipes:
        all_ingredients = recipe['ingredients']
        all_ingredients = all_ingredients.strip().split(',')
        print(recipe['title'].strip())
        for ingredient in all_ingredients:
            print('\t{}'.format(ingredient.strip()))


if __name__ == '__main__':
    get_recipes('onion, olive oil, cheese')
