# 1st step import modules
import requests
import csv
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver

series_name = []
rate = []
episode = []
published_year = []

url = "https://mydramalist.com/dramalist/11979985"
page = requests.get(url)
src = page.content
soup = BeautifulSoup(src, "lxml")
completed_series = soup.find("div",{"class":"mdl-style-list mdl-style-list-2 box"})
series_names = completed_series.find_all("td",{"class":"mdl-style-col-title sort1"})
rates = completed_series.find_all("span",{"class":"score"})
episodes = completed_series.find_all("span",{"class":"episode-total"})
published_years = completed_series.find_all("td",{"class":"mdl-style-col-year sort3 hidden-sm-down"})

for i in range(len(series_names)):
        series_name.append(series_names[i].text.strip())
        rate.append(rates[i].text.strip())
        episode.append(episodes[i].text.strip())
        published_year.append(published_years[i].text.strip())

file_list = [series_name,rate,episode,published_year]
exported = zip_longest(*file_list)
file_path = r"D:\Projecrs\VS Code\Python\Wep Scraping\My_Drama_List\My_Drama_List.csv"
with open (file_path, "w", newline='', encoding='utf-8') as Drama :
           wr = csv.writer(Drama)
           wr.writerow(["Series","Rate","Episodes","Published_Year"])
           wr.writerows(exported)