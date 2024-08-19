import requests
import csv
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver

i = 1
episode = int(input("Enter episodes : "))
name = input("Enter the name of series : ")
name_with_dash = name.replace(" ", "-")
series_name = []
down = []
uppom = []
while i <= episode:
    page = requests.get(f"https://egybest.onl/series-presumed-innocent-season-1-episode-{i}-1/")
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    try:
        down_links = soup.find("article",{"class":"main-article download-section"}).find("a",{"rel":"nofollow"}).attrs['href']
        down.append(down_links)
    except:
        down.append("Not Found")
        print("No links found")
    
    series_name.append(f"{name} ep{i}")
    i += 1
for link in down:
    page = requests.get(link)
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    uppom_links = soup.find("div",{"class":"flex-center align-center"}).find("a").attrs['href']
    uppom.append(uppom_links)




file_list = [series_name,uppom]
exported = zip_longest(*file_list)
file_path = rf"D:\Projecrs\VS Code\Python\Wep Scraping\Egybest\{name}.csv"
with open(file_path, "w", newline='', encoding='utf-8') as Egybest:
    wr = csv.writer(Egybest)
    wr.writerow(["series_name","uppom"])
    wr.writerows(exported)