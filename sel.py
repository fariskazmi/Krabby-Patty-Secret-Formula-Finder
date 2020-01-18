import sys
sys.path.append(r"C:\Users\vince\AppData\Local\Programs\Python\Python37\Lib\site-packages")

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install()) #get driver

TEAMS = [] #init lists
SCORES = []
RECORDS = []

#prep website
date = "2020-01-12" #input("Get scores for which date? (YEAR-MONTH-DAY, ex: Jan. 10 = 2020-01-12): ")

website = "https://ca.global.nba.com/scores/#!/" + date 

driver.get(website)
