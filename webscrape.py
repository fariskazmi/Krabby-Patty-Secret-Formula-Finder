import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://www.foodnetwork.com/recipes/ellie-krieger/breakfast-burrito-recipe-1953146'
response = requests.get(url)
driver.get(url)

'''
soup = BeautifulSoup(response.text, 'html.parser')

# find all elements beginning with the following
ingred_h = soup.find_all(class_='o-Ingredients__a-Ingredient')

# get list of ingredients as a string
ingredients = []
for i in range(len(ingred_h)):
    ingredients.append(str(ingred_h[i].get_text()))

for ingredient in ingredients:
    print(ingredient)
'''