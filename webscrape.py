import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import json
#import pandas as pd
#import time
from termcolor import colored
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimp



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
 #   print(colored('Search Page Loaded Successfully!', 'yellow'))

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
 #               print(colored('Found Recipe!', 'yellow'))
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

  #  print(colored('Recipe Page Loaded Successfully!', 'yellow'))

    soup = BeautifulSoup(response.text, 'html.parser')

    # get recipe info
    title = get_recipe_title(soup)
    ingredients = get_ingredients(soup)
    steps = get_directions(soup)

    # construct recipe as a dictionary
    recipe = {'title':title, 'ingredients':ingredients, 'steps':steps, 'url':url}

    return recipe

def write_json_file(recipe):
    '''
    Description: write recipe information as a JSON text file.

    Arguments:
        recipe (dict): dictionary containing all recipe info
    '''
    with open('recipe_json', 'w') as json_file:
        json.dump(recipe, json_file)

### MAIN ###
if __name__ == "__main__":

    #prompt user
    print(colored('Welcome to Krabby Patty Secret Formula Finder!', 'yellow'))
    print(colored('Enter a dish:', 'yellow'), end=' ')
    dish = input()

 #   print(colored('\nOkay! Looking for recipe...', 'yellow'))

    url = search_recipe_url(dish)
    # check if url exists (recipe exists)
    if url:
        recipe = read_recipe(url)
        show_recipe(recipe)
        write_json_file(recipe)

    elif dish.lower() == 'krabby patty':
        print(colored('Nice try, Plankton >:D', 'red'))
    else:
        print(colored('Recipe not found :(', 'red'))
