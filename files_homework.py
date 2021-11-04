from pathlib import Path
from pprint import pprint
import json

CUR_DIR = Path(__file__).resolve().parent
DATA = CUR_DIR / "recipes.txt"

def get_data(file):
    """Getting data inside a file and spliting data inside the file in lists on empty strings

    Args:
        file (.txt): file with .txt extension

    Returns:
        list: list of data
    """

    with open(file, "r", encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
        # Adding an empty string at the end of the "lines" list, will be used to wrap everything between the second to last and the last string in a list
        lines.append('')

    # Wrap all strings between two empty strings in a list of strings (data_inside), first string doesn't need to be empty
    data =[]
    data_inside=[]
    for line in lines:
        if line != '':
            data_inside.append(line)
        else:
            data.append(data_inside)
            data_inside = []

    return data


def make_cook_book(data_ : list) -> dict:
    """Create a dictionnary out of a list. In the dictionnary each key has a list of dictionnary

    Args:
        data_ (list): list containing lists

    Returns:
        dict: Dictionnary made out of a list containing lists
    """
    book_ = {}
    for i in range(len(data_)):
        ingredients = []
        a, b, *args = data_[i]
        # args should contain strings with two " | " separators inside like "Egg | 1 | pc"
        for elem in args:
            massif = elem.split(' | ')
            ingredients.append(dict(ingredient_name = massif[0], quantity = massif[1], measure = massif[2]))
        book_[a] = ingredients
    return book_
        
        
def get_shop_list_by_dishes(dishes : list, person_count : int) -> dict:
    """Create a dictionnary of needed ingredients to cook dishes for a number of person

    Args:
        dishes (list): list of dishes
        person_count (int): Number of people

    Returns:
        dict: Dictionnary of ingredients
    """
    cook_book =  make_cook_book(get_data(DATA))
    ingredients = []
    for dish in dishes:
        ingredients.extend(cook_book.get(dish))
    # pprint(ingredients)

    ingredients_dict = {}
    for elem in ingredients:
        ingredient_name = elem.get('ingredient_name')
        if ingredient_name not in ingredients_dict:
            ingredients_dict[ingredient_name] = dict(quantity = int(elem.get('quantity')) * person_count, measure = elem.get('measure'))
        else:
            existing_ingredient = ingredients_dict.get(ingredient_name)
            quantity_to_add = int(existing_ingredient.get('quantity'))
            ingredients_dict[ingredient_name] = dict(quantity = quantity_to_add + int(elem.get('quantity')) * person_count, measure = elem.get('measure'))
    
    return ingredients_dict


pprint(get_shop_list_by_dishes(dishes=['Запеченный картофель', 'Омлет'], person_count=2))

# with open('Ingredients.json', 'w', encoding='utf-8-sig') as f:
#     json.dump(get_shop_list_by_dishes(dishes=['Запеченный картофель', 'Омлет'], person_count=2), f, ensure_ascii=False, indent=4)

