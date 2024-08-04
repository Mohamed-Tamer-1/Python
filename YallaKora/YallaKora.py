import requests
import csv
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver

# webdriver_path = r'C:\Program Files (x86)\Google\chromedriver.exe'
# driver = webdriver.Chrome()
# driver.maximize_window()
date = input("Enter Date in this Format (MM/DD/YYYY)")
title = []
stage = []
team_a = []
team_b = []
score = []
channel = []
_time = []
match_details = []

url = f"https://www.yallakora.com/match-center/%d9%85%d8%b1%d9%83%d8%b2-%d8%a7%d9%84%d9%85%d8%a8%d8%a7%d8%b1%d9%8a%d8%a7%d8%aa?date={date}#"
# driver.get(url)
page = requests.get(url)
src = page.content
soup = BeautifulSoup(src, 'lxml')
copa_america = soup.find("div",{"class":"2898 matchCard matchesList"})
euro = soup.find("div",{"class":"2871 matchCard matchesList"})
egy_league = soup.find("div",{"class":"2846 matchCard matchesList"})
def euro_champion(euro):
    titles = euro.find("a",{"class":"tourTitle"}).find("h2").text.strip()
    stages = euro.find("div",{"class":"date"})
    team_A = euro.find_all("div",{"class":"teams teamA"})
    team_B = euro.find_all("div",{"class":"teams teamB"})
    result = euro.find_all("div",{"class":"MResult"})
    channels = euro.find_all("div",{"class":"channel icon-channel"})
    for i in range(len(team_A)):
        title.append(titles)
        stage.append(stages.text.strip())
    if channels:
        for i in channels:
            channel.append(i.text.strip())
    else:
        channels = copa_america.find_all("div",{"class":"channel icon-channel"})
        for i in channels:
            channel.append("")
    for i in team_A:
        team_a.append(i.find("p").text.strip())
    for i in team_B:
        team_b.append(i.find("p").text.strip())
    for scor in result:
        sc = scor.find_all("span",{"class":"score"})
        times = scor.find("span",{"class":"time"})
        _time.append(times.text.strip())
        formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
        score.append(formatted_score)
def copa_america_champion(copa_america):
    titles = copa_america.find("a",{"class":"tourTitle"}).find("h2").text.strip()
    stages = copa_america.find("div",{"class":"date"})
    team_A = copa_america.find_all("div",{"class":"teams teamA"})
    team_B = copa_america.find_all("div",{"class":"teams teamB"})
    result = copa_america.find_all("div",{"class":"MResult"})
    channels = copa_america.find_all("div",{"class":"channel icon-channel"})
    for i in range(len(team_A)):
        title.append(titles)
        stage.append(stages.text.strip())
    if channels:
        for i in channels:
            channel.append(i.text.strip())
    else:
        channels = egy_league.find_all("div",{"class":"channel icon-channel"})
        for i in channels:
            channel.append("")
    for i in team_A:
        team_a.append(i.find("p").text.strip())
    for i in team_B:
        team_b.append(i.find("p").text.strip())
    for scor in result:
        sc = scor.find_all("span",{"class":"score"})
        times = scor.find("span",{"class":"time"})
        _time.append(times.text.strip())
        formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
        score.append(formatted_score)
def egy_league_champion(egy_league):
    titles = egy_league.find("a",{"class":"tourTitle"}).find("h2").text.strip()
    stages = egy_league.find("div",{"class":"date"})
    team_A = egy_league.find_all("div",{"class":"teams teamA"})
    team_B = egy_league.find_all("div",{"class":"teams teamB"})
    result = egy_league.find_all("div",{"class":"MResult"})
    channels = egy_league.find_all("div",{"class":"channel icon-channel"})
    for i in range(len(team_A)):
        title.append(titles)
        stage.append(stages.text.strip())
    for i in channels:
         channel.append(i.text.strip())
    for i in team_A:
        team_a.append(i.find("p").text.strip())
    for i in team_B:
        team_b.append(i.find("p").text.strip())
    for scor in result:
        sc = scor.find_all("span",{"class":"score"})
        times = scor.find("span",{"class":"time"})
        _time.append(times.text.strip())
        formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
        score.append(formatted_score)
            
euro_champion(euro)
copa_america_champion(copa_america)
egy_league_champion(egy_league)

# driver.quit()

file_list = [title, stage, team_a, team_b, _time, score, channel]
file_path = r"D:\Projecrs\VS Code\Python\Wep Scraping\YallaKora\YallaKora.csv"
exported =  zip_longest(*file_list)
with open(file_path, 'w', newline='', encoding='utf-8-sig') as YallaKora:
    wr = csv.writer(YallaKora)
    wr.writerow(["Champion", "Stage", "Team A", "Team B", "Time", "Score", "Channel"])
    wr.writerows(exported)
