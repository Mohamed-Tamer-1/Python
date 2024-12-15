# 1st step import modules
import requests
import csv
import time
import os
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()

page_num = 0
job_title = []
company_name = []
location = []
poste = []
employment_statuse = []
salary = []
skill = []
job_categorie = []
job_Description = []
job_requirment = []
links = []
while True:
    url = f"https://wuzzuf.net/search/jobs/?a=spbg&q=python&start={page_num}"
    # 2nd step use requests to fetch the url
    driver.get(url)

    # 3rd step save page content markup
    src = driver.page_source.encode('utf-8').strip()

    # 4th step create soup object to parse content
    soup = BeautifulSoup(src, "lxml")

    # 5th step find the elements containing info we need 
    page_limit = int(soup.strong.text)
    if (page_num > (page_limit//15)):
          break
    job_titles = soup.find_all("h2", {"class":"css-m604qf"})    
    company_names = soup.find_all("a", {"class":"css-17s97q8"})
    postes_old = soup.find_all("div",{"class":"css-do6t5g"})
    postes_new = soup.find_all("div",{"class":"css-4c4ojb"})
    postes = [*postes_old, *postes_new]
    locations = soup.find_all("span", {"class":"css-5wys0k"})
    # 6th extract information into lists
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text)
        company_name.append(company_names[i].text.replace("-",""))
        location.append(locations[i].text)
        poste.append(postes[i].text)
        links.append(job_titles[i].find("a").attrs['href'])
    page_num += 1
    print("page switched")
    break

for link in links :
    driver.get(link)
    time.sleep(2)
    src = driver.page_source
    soup = BeautifulSoup(src,"lxml")
    employment_statuses = soup.find("div",{"class":"css-5kov97"})
    employment_statuse.append(employment_statuses.text.strip())
    salaries = soup.find_all("span",{"class":"css-4xky9y"})
    fouth_div = salaries[3]
    salary_text = [salary.text.strip() for salary in fouth_div]
    salary.append(', '.join(salary_text))
    skills = soup.find_all("span",{"class":"css-tt12j1 e12tgh591"})
    skill_text = [skill.text.strip() for skill in skills]
    skill.append(', '.join(skill_text))  # join the skills with commas
    job_Descriptions = soup.find("div",{"class":"css-1uobp1k"})
    if job_Descriptions :
          job_Description.append(job_Descriptions.text.strip())
    else :
        job_Description.append("N/A")
    job_requirments = soup.find("div",{"class":"css-1t5f0fr"})
    if job_requirments :
        job_requirment.append(job_requirments.text.strip())
    else :
        job_requirment.append("N/A")
    job_categories = soup.find("span",{"class":"css-158icaa"})
    job_categorie.append(job_categories.text.strip())

driver.quit()

# 7th creat csv file and fill it with values
file_list = [job_title, company_name, location, poste, employment_statuse, salary, skill, job_categorie, job_requirment, job_Description, links]
exported = zip_longest(*file_list)
current_directory = os.getcwd()
csv_file = os.path.join(current_directory, f"YallaKora.csv")
with open (csv_file, "w", newline='', encoding='utf-8') as jobs :
           wr = csv.writer(jobs)
           wr.writerow(["job_title","company_name","location","posted","employment statuses","salary","skill","job_categorie","job_requirment","job_Description","link"])
           wr.writerows(exported)
