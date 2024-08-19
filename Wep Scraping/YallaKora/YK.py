import requests
import csv
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver

# webdriver_path = r'C:\Program Files (x86)\Google\chromedriver.exe'
# driver = webdriver.Chrome()
# driver.maximize_window()
date = input("Enter Date in this Format (MM/DD/YYYY): ")
title = []
team_a = []
team_b = []
score = []

url = f"https://www.yallakora.com/match-center/%d9%85%d8%b1%d9%83%d8%b2-%d8%a7%d9%84%d9%85%d8%a8%d8%a7%d8%b1%d9%8a%d8%a7%d8%aa?date={date}#"
# driver.get(url)
page = requests.get(url)
src = page.content
soup = BeautifulSoup(src, 'lxml')

titles = soup.find_all("a",{"class":"tourTitle"})
num_of_champions = soup.find_all("div",{"class":"ul"})
for champion in num_of_champions:
    num_of_matches_not_played = champion.find_all("div",{"class":"item future liItem"})
    num_of_matches_played = champion.find_all("div",{"class":"item finish liItem"})
    for match in num_of_matches_not_played: 
        team_A = match.find_all("div",{"class":"teams teamA"})
        team_B = match.find_all("div",{"class":"teams teamB"})
        result = match.find_all("div",{"class":"MResult"})
        for i in team_A:
            team_a.append(i.find("p").text.strip())
        for i in team_B:
            team_b.append(i.find("p").text.strip())
        for scor in result:
            sc = scor.find_all("span",{"class":"score"})
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)
    # matches that played
    for match in num_of_matches_played: 
        team_A = match.find_all("div",{"class":"teams teamA"})
        team_B = match.find_all("div",{"class":"teams teamB"})
        result = match.find_all("div",{"class":"MResult"})
        for i in team_A:
            team_a.append(i.find("p").text.strip())
        for i in team_B:
            team_b.append(i.find("p").text.strip())
        for scor in result:
            sc = scor.find_all("span",{"class":"score"})
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)
for t in titles[:len(team_a)]:
    title.append(t.text.strip())                

# driver.quit()

file_list = [title,team_a, team_b, score]
file_path = r"D:\Projecrs\VS Code\Python\Wep Scraping\YallaKora\YK.csv"
exported =  zip_longest(*file_list)
with open(file_path, 'w', newline='', encoding='utf-8-sig') as YK:
    wr = csv.writer(YK)
    wr.writerow(["title","Team A", "Team B", "Score"])
    wr.writerows(exported)
