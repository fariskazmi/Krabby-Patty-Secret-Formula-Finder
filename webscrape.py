import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import numpy as np
from matplotlib import pyplot as plt
from random import seed
from random import random
import datetime

import tensorflow.compat.v1 as tf
import PIL

import json
from termcolor import colored
import uuid

def image_classifier():
    '''
    Description: Takes an image from a Google drive, then uses the MobileNet model available in Tensorflow to return a classification of the image
    '''
    name = str(uuid.uuid4())
    file = tf.keras.utils.get_file(origin= 'https://drive.google.com/uc?export=view&id=11N3E8gj26I8-PBNh8QJkcL0vYKQh3zxS', fname= name)
    print(type(file))
    print(file)
    img = tf.keras.preprocessing.image.load_img(file, target_size=[224, 224])
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet.preprocess_input(
    x[tf.newaxis,...])
    labels_path = tf.keras.utils.get_file(
    'ImageNetLabels.txt',
    'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
    imagenet_labels = np.array(open(labels_path).read().splitlines())
    pretrained_model = tf.keras.applications.MobileNet()
    result_before_save = pretrained_model(x)
    decoded = imagenet_labels[np.argsort(result_before_save)[0,::-1][:5]+1]

    if decoded[0] != 'cheeseburger':
        print(colored(decoded[0], 'yellow'))
    else:
        print(colored('KRABBY PATTY', 'yellow'))

    return decoded[0]

def search_recipe_url(dish):
    '''
    Description: Access search page of Food Network using the name of the dish, then get url of the chosen recipe

    Arguments:
        dish (string): name of the dish to type in the search engine

    Returns:
        (string): url of the chosen recipe. Returns NoneType if recipe is not found.
    '''
    # replace space with hyphens and add a hyphen at the end
    dish = dish.replace(' ', '-').lower()
    dish += '-'

    # search page url
    url = 'https://www.foodnetwork.com/search/' + dish

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # get each result
    search_results = soup.find_all('div', {'class': 'm-MediaBlock__m-TextWrap'})

    for result in search_results:

        # identify whether the result is a "recipe" page
        page_type = result.find(class_='m-Info__a-SubHeadline')
        if page_type is not None:

            # obtain and return the url of the recipe
            if page_type.get_text() == 'Recipe':
                link = result.find('a', {'href': re.compile("^//www.foodnetwork.com/recipes/")})
                return 'https:' + link.get('href')
    
    # if recipe is not found, return NoneType
    return None

def get_recipe_title(soup):
    '''
    Description: Obtains the title of the recipe

    Arguments:
        soup (BeautifulSoup): BeautifulSoup instance (of the recipe webpage)

    Returns:
        (string): recipe title
    '''
    return soup.find(class_='o-AssetTitle__a-HeadlineText').get_text()

def get_ingredients(soup):
    '''
    Description: Obtains ingredients of the recipe.

    Arguments:
        soup (BeautifulSoup): BeautifulSoup instance (of the recipe webpage)

    Returns:
        ingredients (list): list of ingredients stored as strings
    '''
    ingred_html = soup.find_all(class_='o-Ingredients__a-Ingredient')

    ingredients = []
    # check if ingredients exist
    if not ingred_html:
        ingredients.append('No Ingredients Found')
    else:
        # get list of ingredients as strings
        for i in range(len(ingred_html)):
            ingredients.append(ingred_html[i].get_text())

    return ingredients

def get_directions(soup):
    '''
    Description: Obtains directions of the recipe.

    Arguments:
        soup (BeautifulSoup): BeautifulSoup instance (of the recipe webpage)

    Returns:
        steps (list): list of directions stored as strings
    '''
    steps_html = soup.find_all(class_='o-Method__m-Step')

    steps = []
    for step_html in steps_html:
        steps.append(step_html.get_text().strip())

    return steps

def show_recipe(recipe):
    '''
    Description: displays recipe info on terminal.

    Arguments:
        recipe (dict): dictionary containing all recipe info
    '''
    print(colored('\nShowing Recipe for: ' + recipe['title'].upper(), 'cyan'))

    # print ingredients
    print(colored('INGREDIENTS:', 'magenta'))
    for ingredient in recipe['ingredients']:
        print(colored(ingredient, 'green'))

    # print directions
    print(colored('\nDIRECTIONS:', 'magenta'))
    for step_num in range(0, len(recipe['steps'])):
        print(colored(str(step_num+1) + ') ' + recipe['steps'][step_num] + '\n', 'green'))
    
    #display url
    print(colored('URL: ' + recipe['url'], 'grey'))

def read_recipe(url):
    '''
    Description: Read information (title, ingredients, directions) on a recipe webpage from given url.

    Arguments:
        url (string): url of the recipe webpage

    Returns:
        recipe (dict): dictionary containing all recipe info
    '''
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # get recipe info
    title = get_recipe_title(soup)
    ingredients = get_ingredients(soup)
    steps = get_directions(soup)

    # construct recipe as a dictionary
    recipe = {'title':title, 'ingredients':ingredients, 'steps':steps, 'url':url}

    return recipe

def no_recipe():
    '''
    Description: Creates a recipe directory for when recipe was not found.

    Returns:
        recipe (dict): dictionary representing that no recipe was found
    '''
    recipe = {'title':'No Recipe Found', 'ingredients':[''], 'directions':[''], 'url':''}
    return recipe

def write_json_file(recipe):
    '''
    Description: write recipe information as a JSON text file.

    Arguments:
        recipe (dict): dictionary containing all recipe info
    '''
    with open('recipe_json', 'w') as json_file:
        json.dump(recipe, json_file)

def post_request(recipe):
    '''
    Description: Creates a post request to send recipe info to an external website

    Arguments:
        recipe (dict): dictionary containing all recipe info
    '''

    url = 'https://us-central1-krabbypatty.cloudfunctions.net/get_json_data_js'

    x = requests.post(url, json = recipe)

    print(x.text)

### MAIN ###
if __name__ == "__main__":

    dish = image_classifier()

    url = search_recipe_url(str(dish))
    # check if url exists (recipe exists)
    if url and (dish.lower() != 'cheeseburger'):
        recipe = read_recipe(url)
        show_recipe(recipe)
        write_json_file(recipe)

    elif dish.lower() == 'cheeseburger':
        print(colored('Nice try, Plankton >:D', 'red'))
        recipe = no_recipe()
    else:
        print(colored('Recipe not found :(', 'red'))
        recipe = no_recipe()

    post_request(recipe)
