import logging
from datetime import datetime
import inspect
current_datetime = datetime.now()

#декорируемая функция
# def foo(i, m):
#     if i == 1:
#         print('Doing some operations')
#         if m == 2:
#             data = 'Get some result'
#     return data

#декоратор-логгер
# def decor(foo):
#     logging.basicConfig(filename="log_output.log", level=logging.INFO)
#     def new_foo(*args, **kwargs):
#         result = foo(*args, **kwargs)
#         log = {}
#         log['data'] = current_datetime
#         function_params = inspect.getfullargspec(decor)
#         log['function_name'] = list(function_params)[0]
#         log['*args'] = args
#         log['*kwargs'] = kwargs
#         log['result'] = result
#         logging.info(log)
#         return result
#     return new_foo

#параметризованный декоратор-логгер
def parametrized_decor(parameter):
    def decor(get_shop_list_by_dishes):
        logging.basicConfig(filename=parameter, level=logging.INFO)
        def new_foo(*args, **kwargs):
            result = get_shop_list_by_dishes(*args, **kwargs)
            log = {}
            log['data'] = current_datetime
            function_params = inspect.getfullargspec(decor)
            log['function_name'] = list(function_params)[0]
            log['*args'] = args
            log['*kwargs'] = kwargs
            log['result'] = result
            logging.info(log)
            return result
        return new_foo
    return decor

#применение логгера к домашнему заданию (написать функцию, формирующую кулинарную книгу из неупорядоченного файла)

from pprint import pprint
from collections import defaultdict

def get_cook_book():
    cook_book = defaultdict(list)
    list_1 = []
    with open("recipes.txt", encoding="utf-8") as file:
         for line in file:
             cook_name = line.strip()
             ingredients_quantity = int(file.readline().strip())
             for ingredient in range(ingredients_quantity):
                 words = file.readline().split()
                 d = defaultdict(list)
                 if len(words) == 5:
                     d['ingredient_name'] = words[0]
                     d['quantity'] = words[2]
                     d['measure'] = words[4]
                     list_1.append(dict(d))
                 else:
                     d['ingredient_name'] = words[0] + ' ' + words[1]
                     d['quantity'] = words[3]
                     d['measure'] = words[5]
                     list_1.append(dict(d))
             cook_book[cook_name] += list_1
             list_1.clear()
             file.readline()
    return dict(cook_book)

person_count = 2
dishes = list(get_cook_book().keys())

@parametrized_decor(parameter='log.txt')
def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for dish in dishes:
        ingredients = get_cook_book()[dish]
        for ingredient in ingredients:
            key = ingredient['ingredient_name']
            measure = ingredient['measure']
            quantity = int(ingredient['quantity']) * person_count
            dict_1 = defaultdict(list)
            dict_1['measure'] = measure
            dict_1['quantity'] = quantity
            shop_list[key] = dict(dict_1)
    return shop_list
pprint(get_shop_list_by_dishes(dishes, person_count))
