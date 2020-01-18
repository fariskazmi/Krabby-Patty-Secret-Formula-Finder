import requests
# from selenium import webdriver
from bs4 import BeautifulSoup
from csv import writer

response = requests.get('https://www.foodnetwork.com/recipes/ellie-krieger/breakfast-burrito-recipe-1953146')

soup = BeautifulSoup(response.text, 'html.parser')

# find all elements beginning with the following
ingredients = []
ingredients.append(soup.find_all(class_='o-Ingredients__a-Ingredient').get_text())

# get list of ingredients as a string
#ingredients = []
#for i in range(len(ingred_h)):
#    ingredients.append(str(ingred_h[i])[39:-4])

for ingredient in ingredients:
    print(ingredient)
