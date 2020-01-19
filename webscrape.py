import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import re
#import pandas as pd
#import time
from termcolor import colored

def search_recipe_url(dish):
    '''
    Description: Access search page of Food Network using the name of the dish, then get url of the chosen recipe

    Arguments:
        dish (string): name of the dish to type in the search engine

    Returns:
        (string): url of the chosen recipe
    '''

    # replace space with hyphens and add a hyphen at the end
    dish = dish.replace(' ', '-').lower()
    dish += '-'

    # search page url
    url = 'https://www.foodnetwork.com/search/' + dish

 #   driver.get(url) # open web page
 #   time.sleep(10) # allow the web to load

    response = requests.get(url)
    print(colored('Search Page Loaded Successfully!', 'yellow'))

    # obtain html of the web
 #   html = driver.page_source

 #   soup = BeautifulSoup(html, 'html.parser')
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
                print(colored('Found Recipe!', 'yellow'))
                return link.get('href')
    
    # if recipe is not found
    print(colored('Recipe not found :(', 'red'))
    return '//www.google.ca'

### MAIN ###
if __name__ == "__main__":

    #prompt user
    print(colored('Welcome to Krabby Patty Secret Formula Finder!', 'yellow'))
    print(colored('Enter a dish:', 'yellow'), end=' ')
    dish = input()

    print(colored('\nOkay! Looking for recipe...', 'yellow'))

 #   driver = webdriver.Chrome(ChromeDriverManager().install())

    url = 'https:' + search_recipe_url(dish)
    
    response = requests.get(url)

 #   driver.get(url)

    # allow the web to load
 #   time.sleep(10)
    print(colored('Recipe Page Loaded Successfully!', 'yellow'))

    # obtain html of the url
 #   html = driver.page_source

 #   soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(response.text, 'html.parser')

    #get recipe title
    title = soup.find(class_='o-AssetTitle__a-HeadlineText').get_text()
    print(colored('\nShowing Recipe for: ' + title.upper(), 'cyan'))

    '''GRAB INGREDIENTS'''
    # find all elements beginning with the following
    ingred_html = soup.find_all(class_='o-Ingredients__a-Ingredient')

    ingredients = []
    # check if ingredients exist
    if not ingred_html:
        ingredients.append('No Ingredients Found')
    else:
        # get list of ingredients as strings
        for i in range(len(ingred_html)):
            ingredients.append(ingred_html[i].get_text())

    # print ingredients
    print(colored('INGREDIENTS:', 'magenta'))
    for ingredient in ingredients:
        print(colored(ingredient, 'green'))

    '''GRAB DIRECTIONS'''
    steps_html = soup.find_all(class_='o-Method__m-Step')
    
    print(colored('\nDIRECTIONS:', 'magenta'))
    for step_num in range(0, len(steps_html)):
        print(colored(str(step_num+1) + ') ' + steps_html[step_num].get_text().strip() + '\n', 'white'))

    #display url
    print(colored('URL: ' + url, 'grey'))
