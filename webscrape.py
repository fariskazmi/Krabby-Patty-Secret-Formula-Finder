#import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import re
#import pandas as pd

import time

driver = webdriver.Chrome(ChromeDriverManager().install())

def search(dish):
    '''
    Description: Access search page of Food Network using the name of the dish, then get url of the chosen recipe

    Arguments:
        dish (string): name of the dish to type in the search engine

    Returns:
        url (string): url of the chosen recipe
    '''

    # replace space with hyphens and add a hyphen at the end
    dish = dish.replace(' ', '-').lower()
    dish += '-'

    # search page url
    url = 'https://www.foodnetwork.com/search/' + dish

    driver.get(url) # open web page
    time.sleep(10) # allow the web to load

    # obtain html of the web
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    search_elements = soup.find_all('a', attrs={'href': re.compile("^https://www.foodnetwork.com/")})

    for link in search_elements:
        print(link.get('href'))

'''
    subheadline = ""
    while subheadline != 'Article':
        subheadline = soup.find_all(class_='m-Info__a-SubHeadline')
        print(subheadline)
'''

search('tea')

'''
url = 'https://www.foodnetwork.com/recipes/ellie-krieger/breakfast-burrito-recipe-1953146'
#response = requests.get(url)
driver.get(url)

# allow the web to load
time.sleep(10)

# obtain html of the url
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

# find all elements beginning with the following
ingred_h = soup.find_all(class_='o-Ingredients__a-Ingredient')

# get list of ingredients as a string
ingredients = []
for i in range(len(ingred_h)):
    ingredients.append(str(ingred_h[i].get_text()))

# print ingredients
for ingredient in ingredients:
    print(ingredient)
'''