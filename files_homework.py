from pathlib import Path
from pprint import pprint
import json

CUR_DIR = Path(__file__).resolve().parent
DATA = CUR_DIR / "recipes.txt"


def get_data(file) -> list:
    """Gets content from a .txt file. Splits the content on empty strings and return a list

    Args:
        file: path to a .txt file

    Returns: list of data
    """
    with open(file, "r", encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
        # Adding an empty string at the end of the "lines" list. Will be used to wrap everything between
        # the second to last and the last empty string
        lines.append('')

    all_meals = []
    meal = []
    for line in lines:
        if line != '':
            meal.append(line)
        else:
            all_meals.append(meal)
            meal = []

    return all_meals


def make_cook_book(data_: list) -> dict:
    """Create a dictionary out of a list. In the dictionary each key has a list of dictionary

    Args:
        data_ (list): list containing lists

    Returns:
        dict: Dictionary made out of a list containing lists
    """
    cook_book = {}
    for i in range(len(data_)):
        ingredients = []
        a, b, *args = data_[i]
        # args should contain strings with two " | " separators inside like "Egg | 1 | pc"
        for arg in args:
            arg_list = arg.split(' | ')
            ingredients.append(dict(ingredient_name=arg_list[0], quantity=arg_list[1], measure=arg_list[2]))
        cook_book[a] = ingredients
    return cook_book


my_cook_book = make_cook_book(get_data(DATA))
print('Список рецептов:')
pprint(my_cook_book)


# with open('recipes.json', 'w', encoding='utf-8-sig') as cook_book_file:
#     json.dump(my_cook_book, cook_book_file,
#               ensure_ascii=False, indent=4)


def get_shop_list_by_dishes(dishes: list, person_count: int) -> dict:
    """Creates a dictionary of needed ingredients to cook dishes for a number of person

    Args:
        dishes (list): list of dishes
        person_count (int): Number of person to cook for

    Returns: Dictionary of ingredients
    """
    cook_book = make_cook_book(get_data(DATA))
    all_ingredients = []
    for dish in dishes:
        all_ingredients.extend(cook_book.get(dish))
    # pprint(all_ingredients)

    ingredients_dict = {}
    for ingredient in all_ingredients:
        ingredient_name = ingredient.get('ingredient_name')
        if ingredient_name not in ingredients_dict:
            ingredients_dict[ingredient_name] = dict(quantity=int(ingredient.get('quantity')) * person_count,
                                                     measure=ingredient.get('measure'))
        else:
            existing_ingredient = ingredients_dict.get(ingredient_name)
            quantity_to_add = existing_ingredient.get('quantity')
            ingredients_dict[ingredient_name] = dict(
                quantity=quantity_to_add + int(ingredient.get('quantity')) * person_count,
                measure=ingredient.get('measure'))

    return ingredients_dict


shop_list = get_shop_list_by_dishes(dishes=['Запеченный картофель', 'Омлет'], person_count=2)
print('\nИнгедиенты:')
pprint(shop_list)

# with open('shop_list.json', 'w', encoding='utf-8-sig') as shop_list_file:
#     json.dump(shop_list, shop_list_file,
#               ensure_ascii=False, indent=4)
