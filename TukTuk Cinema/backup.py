import requests
import csv
import os
import time
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

# Initialize WebDriver
webdriver_path = r'C:\Program Files (x86)\Microsoft\msedgedriver.exe'

# Path to the ad blocker extension (e.g., AdBlock or uBlock Origin)
ad_blocker_extension_path = r"C:\Users\Me\AppData\Local\Microsoft\Edge\User Data\Default\Extensions\odfafepnkmbhccpbejgmiehpchacaeak\1.57.2_0"  # Update with the path to your .zip or .crx file

# Initialize Edge options
edge_options = EdgeOptions()
edge_options.add_argument(f"--load-extension={ad_blocker_extension_path}")

# Initialize Edge WebDriver with the specified options
service = EdgeService(executable_path=webdriver_path)
driver = webdriver.Edge(service=service, options=edge_options)
driver.maximize_window()

url = "https://t40.tuktukcinema1.buzz/%D9%85%D8%B3%D9%84%D8%B3%D9%84-%D8%AD%D8%A8%D9%8A%D8%A8%D9%8A-%D8%B9%D8%B6%D9%88-%D8%A7%D9%84%D8%B9%D8%B5%D8%A7%D8%A8%D8%A9-%D8%A7%D9%84%D9%84%D8%B7%D9%8A%D9%81-my-sweet-mobster-%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-1/watch/"
driver.get(url)

megamax_link_found = False
upstream_link_found = False
mixdrop_link_found = False
name = "x"
megamax = []
upstream = []
mixdrop = []
names = []
epi =1

for episode in range(1, epi + 1):
    try:
        download_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.watchAndDownlaod"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        driver.execute_script("arguments[0].click();", download_button)
    except (ElementClickInterceptedException, TimeoutException):
        print("Run Successfully")
    try:
        src = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(src, "lxml")
        
        link_section = soup.find('div', {'class': 'downloads'})
        if link_section:
            links = link_section.find_all('a')
            
            for link_tag in links:
                span = link_tag.find("span")
                if span and "Megamax" in span.get_text():
                    megamax_link = link_tag['href']
                    megamax.append(megamax_link)
                    megamax_link_found = True
                elif span and "Upstream" in span.get_text():
                    upstream_link = link_tag['href']
                    try:
                        if upstream_link :
                            response = requests.get(upstream_link)
                            soup = BeautifulSoup(response.content, 'lxml')
                            try:
                                upstream_down = soup.find("table", {"class": "table table-borderless"}).find("a").attrs['href']
                                if upstream_down:
                                    upstream.append(upstream_down) 
                                    upstream_link_found = True
                                else:
                                    print("Upstream not found 1")
                            except:
                                print("Upstream not found 2")
                    except:
                        print("Upstream not found 3")
            if not megamax_link_found:
                megamax.append("Not Found")
            if not upstream_link_found:
                upstream.append("Not Found")

            if megamax_link_found or upstream_link_found:
                names.append(f"{name} E{episode}")
        else:
            print("No link selection found")
        if episode < epi:
            try:
                download_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                driver.execute_script("arguments[0].click();", download_button)
            except (ElementClickInterceptedException, TimeoutException):
                print("Download button not clickable or not found")
                break

    except Exception as e:
        print(f"Something went wrong for episode {episode}: {e}")
        break
for link in megamax:
    driver.get(link)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src, "lxml")
    try:
        download_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.v-card-text"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        driver.execute_script("arguments[0].click();", download_button)
    except (ElementClickInterceptedException, TimeoutException):
        print("Download button 720p not clickable or not found")
        break
    time.sleep(2)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src, "lxml")
    links = soup.find_all("div",{"class":"v-virtual-scroll__item"})
    for link_tag in links:
        span = link_tag.find("div",{"class":"v-list-item-title"}).text.strip()
        if span and "mixdrop" in span:
            mixdrop_link_a = link_tag.find("div",{"class":"v-list-item__append"}).find("a")
            mixdrop_link = mixdrop_link_a['href']
            mixdrops = mixdrop_link + "?download"
            mixdrop.append(mixdrops)
            mixdrop_link_found = True
            
    if not mixdrop_link_found:
                mixdrop.append("Not Found")
    




driver.quit()

file_list = [names,upstream,mixdrop]
exp = zip_longest(*file_list)
current_directory = os.getcwd()
csv_file = os.path.join(current_directory, f"TukTuk Cinema.csv")
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "upstream", "mixdrop"])
    writer.writerows(exp)
