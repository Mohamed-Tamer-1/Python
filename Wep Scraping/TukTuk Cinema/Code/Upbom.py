import requests
import csv
import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from bs4 import BeautifulSoup
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains

script_dir = os.path.dirname(os.path.abspath(__file__))
webdriver_path = os.path.join(script_dir, r"Extensions\msedgedriver.exe")
ad_blocker_extension_path = os.path.join(script_dir, r"Extensions\uBlock-Origin.crx")
IDM_extension_path = os.path.join(script_dir, r"Extensions\IDM-Integration-Module.crx")
# webdriver_path = r"D:\Code\Extensions\msedgedriver.exe"
# ad_blocker_extension_path = r"D:\Code\Extensions\uBlock-Origin.crx"
# IDM_extension_path = r"D:\Code\Extensions\IDM-Integration-Module.crx"


download_dir = os.path.join(os.getcwd(), "downloads")  # Set download directory to the script's directory
if not os.path.exists(download_dir):
    os.makedirs(download_dir)
# Initialize WebDriver
# profile_path = r"C:\Users\Me\AppData\Local\Microsoft\Edge\User Data\Default\Personal"  # Update with your Edge profile path
# edge_options.add_argument(f"user-data-dir={profile_path}")

def wait_for_download(download_path, file_names):
    all_files_exist = False
    while not all_files_exist:
        # Check if all files are downloaded
        all_files_exist = all(os.path.exists(os.path.join(download_path, file_name)) for file_name in file_names)
        if not all_files_exist:
            time.sleep(1)
    return True

# Path to the ad blocker extension (e.g., AdBlock or uBlock Origin)
# Initialize Edge options
edge_options = EdgeOptions()
edge_options.add_extension(ad_blocker_extension_path)
edge_options.add_extension(IDM_extension_path)
prefs = {"download.default_directory": download_dir}
edge_options.add_experimental_option("prefs", prefs)

# Initialize Edge WebDriver with the specified options
service = EdgeService(executable_path=webdriver_path)
driver = webdriver.Edge(service=service, options=edge_options)
driver.maximize_window()

def get_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    global url
    url = simpledialog.askstring("URL", "Enter url:")
    if url is None:
        messagebox.showerror("Input Error", "No input provided for url.")
        root.destroy()
        return
    
    global epi
    epi = simpledialog.askinteger("Episode", "Enter episodes:")
    if epi is None:
        messagebox.showerror("Input Error", "No input provided for episodes.")
        root.destroy()
        return
    
get_input()
# url = "https://t40.tuktukcinema1.buzz/%D9%85%D8%B3%D9%84%D8%B3%D9%84-presumed-innocent-%D8%A7%D9%84%D9%85%D9%88%D8%B3%D9%85-%D8%A7%D9%84%D8%A7%D9%88%D9%84-%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-1/"
driver.get(url)
windows = driver.window_handles
if len(windows) > 1:
    driver.switch_to.window(windows[1])
    driver.close()
    driver.switch_to.window(windows[0])

megamax_link_found = False
upstream_link_found = False
upbom_link_found = False
attempt = 0
max_attempts = 2
megamax = []
upstream = []
upbom = []
series_name = []
D_upbom = []
# epi =3



for episode in range(1, epi + 1):
    current_url = driver.current_url
    if "watch/" not in current_url:
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
                
            if not megamax_link_found:
                megamax.append("Not Found")
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

    except Exception as e:
            print(f"Something went wrong for episode {episode}: {e}")
for link in megamax:
    driver.get(link)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src, "lxml")
    try:
        download_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '720p') or contains(text(), '720p (source)')]"))
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
        if span and "upbom" in span:
            upbom_link_a = link_tag.find("div",{"class":"v-list-item__append"}).find("a")
            upbom_link = upbom_link_a['href']
            upboms = "https:" + upbom_link
            print(upboms)
            upbom.append(upboms)
for link in upbom:
    driver.get(link)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src, "lxml")
    try:
        series_names = soup.find("div",{"class":"tbl-c c-l title"}).find("b").text.strip()
        series_name.append(series_names.replace(" ","_"))
    except AttributeError:
        print("erorr na,e")
    for attempt in range(max_attempts):
        time.sleep(5)
        try:
            # Wait for the element to be clickable
            download_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn3.download-btn"))
            )

            # Use ActionChains to perform the click
            actions = ActionChains(driver)
            actions.move_to_element(download_button).click().perform()
            
            print("Download button clicked successfully.")
        except (ElementClickInterceptedException, TimeoutException):
            print("Download button not clickable or not found in upbom in second page")

file_name = list(set(series_name))
print(file_name)
driver.quit()


file_list = [series_name,D_upbom]
exp = zip_longest(*file_list)
current_directory = os.getcwd()
csv_file = os.path.join(current_directory, f"TukTuk Cinema.csv")
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "upbom"])
    writer.writerows(exp)
