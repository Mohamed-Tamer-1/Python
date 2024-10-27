from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import json
from itertools import zip_longest
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
webdriver_path = os.path.join(script_dir, r"Extensions\chromedriver.exe")
# Set up Chrome options
chrome_options = Options()
# Initialize WebDriver
service = Service(executable_path=webdriver_path)  # Add path to chromedriver if needed
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

date = input("Enter Date in this Format (MM/DD/YYYY): ")
title = []
team_a = []
team_b = []
_timee = []
stages = []
channels = []
score = []

url = f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#"
driver.get(url)

# Wait for the page to load necessary elements
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tourTitle")))

# Get the data
titles = driver.find_elements(By.CLASS_NAME, "tourTitle")
num_of_champions = driver.find_elements(By.CLASS_NAME, "ul")

for champion in num_of_champions:
    num_of_matches_not_played = champion.find_elements(By.CLASS_NAME, "item.future.liItem")
    num_of_matches_played = champion.find_elements(By.CLASS_NAME, "item.finish.liItem")

    # Matches not played
    for match in num_of_matches_not_played:
        team_A = match.find_elements(By.CLASS_NAME, "teams.teamA")
        team_B = match.find_elements(By.CLASS_NAME, "teams.teamB")
        result = match.find_elements(By.CLASS_NAME, "MResult")
        _time = match.find_elements(By.CLASS_NAME, "time")
        stage = match.find_elements(By.CLASS_NAME, "date")
        channel = match.find_elements(By.CLASS_NAME, "channel.icon-channel")
        
        for i in team_A:
            team_a.append(i.find_element(By.TAG_NAME, "p").text.strip())
        for i in team_B:
            team_b.append(i.find_element(By.TAG_NAME, "p").text.strip())
        for i in _time:
            _timee.append(i.text.strip())
        for i in stage:
            stages.append(i.text.strip())
        for i in channel:
            channels.append(i.text.strip())
        for scor in result:
            sc = scor.find_elements(By.CLASS_NAME, "score")
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)

    # Matches played
    for match in num_of_matches_played:
        team_A = match.find_elements(By.CLASS_NAME, "teams.teamA")
        team_B = match.find_elements(By.CLASS_NAME, "teams.teamB")
        result = match.find_elements(By.CLASS_NAME, "MResult")
        _time = match.find_elements(By.CLASS_NAME, "time")
        stage = match.find_elements(By.CLASS_NAME, "date")
        channel = match.find_elements(By.CLASS_NAME, "channel.icon-channel")
        
        for i in team_A:
            team_a.append(i.find_element(By.TAG_NAME, "p").text.strip())
        for i in team_B:
            team_b.append(i.find_element(By.TAG_NAME, "p").text.strip())
        for i in _time:
            _timee.append(i.text.strip())
        for i in stage:
            stages.append(i.text.strip())
        for i in channel:
            channels.append(i.text.strip())
        for scor in result:
            sc = scor.find_elements(By.CLASS_NAME, "score")
            formatted_score = f"{sc[0].text.strip()}  –  {sc[1].text.strip()}"
            score.append(formatted_score)

for t in titles[:len(team_a)]:
    title.append(t.text.strip())

# Close the browser
driver.quit()

# Saving data to CSV
file_list = [stages, team_a, team_b, _timee, score]
current_directory = os.getcwd()
csv_file = os.path.join(current_directory, f"YallaKora.csv")
exported = zip_longest(*file_list)

with open(csv_file, 'w', newline='', encoding='utf-8-sig') as YK:
    wr = csv.writer(YK)
    wr.writerow(["Stage", "Team A", "Team B", "Time", "Score"])
    wr.writerows(exported)

# Save to JSON
json_data = []
for i in range(len(title)):
    match = {
        "Stage": stages[i],
        "Team A": team_a[i],
        "Team B": team_b[i],
        "Time": _timee[i],
        "Score": score[i],
        "Channel": channels[i],
    }
    json_data.append(match)

json_file = os.path.join(current_directory, f"YallaKora.json")
with open(json_file, 'w', encoding='utf-8') as json_out:
    json.dump(json_data, json_out, ensure_ascii=False, indent=4)
