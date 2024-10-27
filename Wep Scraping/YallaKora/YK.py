import math
import requests
import json
import csv
import time
import os
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
_timee = []
stages = []
channels = []
score = []

url = f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#"
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
        _time = match.find_all("span",{"class":"time"})
        stage =  match.find_all("div",{"class":"date"})
        channel = match.find_all("div",{"class":"channel icon-channel"})
        for i in team_A:
            team_a.append(i.find("p").text.strip())
        for i in team_B:
            team_b.append(i.find("p").text.strip())
        for i in _time:
            _timee.append(i.text.strip())
        for i in stage:
            stages.append(i.text.strip())
        for i in channel:
            channels.append(i.text.strip())
        for scor in result:
            sc = scor.find_all("span",{"class":"score"})
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)
        
    # matches that played
    for match in num_of_matches_played: 
        team_A = match.find_all("div",{"class":"teams teamA"})
        team_B = match.find_all("div",{"class":"teams teamB"})
        result = match.find_all("div",{"class":"MResult"})
        _time = match.find_all("span",{"class":"time"})
        stage =  match.find_all("div",{"class":"date"})
        channel = match.find_all("div",{"class":"channel icon-channel"})
        for i in team_A:
            team_a.append(i.find("p").text.strip())
        for i in team_B:
            team_b.append(i.find("p").text.strip())
        for i in _time:
            _timee.append(i.text.strip())
        for i in stage:
            stages.append(i.text.strip())
        for i in channel:
            channels.append(i.text.strip())
        for scor in result:
            sc = scor.find_all("span",{"class":"score"})
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)
for t in titles[:len(team_a)]:
    title.append(t.text.strip())                

# driver.quit()
file_list = [title,stages, team_a, team_b, _timee, score]
current_directory = os.getcwd()
csv_file = os.path.join(current_directory, f"YallaKora.csv")
exported =  zip_longest(*file_list)
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as YK:
    wr = csv.writer(YK)
    wr.writerow(["title","Team A", "Team B", "Score"])
    wr.writerows(exported)

# Save to JSON
json_data = []
for i in range(len(title)):
    match = {
        "Champion": title[i],
        "stage": stages[i],
        "Team A": team_a[i],
        "Team B": team_b[i],
        "Time": _timee[i],
        "Score": score[i],
        "channel": channels[i],
    }
    json_data.append(match)

json_file = os.path.join(current_directory, f"YallaKora.json")
with open(json_file, 'w', encoding='utf-8') as json_out:
    json.dump(json_data, json_out, ensure_ascii=False, indent=4)
