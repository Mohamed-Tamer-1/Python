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
def get_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    global episode
    episode = simpledialog.askinteger("Episode", "Enter episodes:")
    if episode is None:
        messagebox.showerror("Input Error", "No input provided for episodes.")
        root.destroy()
        return

get_input()
webdriver_path = r'C:\Program Files (x86)\Microsoft\msedgedriver.exe'

ad_blocker_extension_path = os.path.join(os.path.dirname(__file__), 'uBlock-Origin.crx')  # Update with the path to your .zip or .crx file
IDM_extension_path = os.path.join(os.path.dirname(__file__), 'IDM-Integration-Module.crx')
edge_options = EdgeOptions()
edge_options.add_extension(ad_blocker_extension_path)
edge_options.add_extension(IDM_extension_path)
service = EdgeService(executable_path=webdriver_path)
driver = webdriver.Edge(service=service, options=edge_options)
driver.maximize_window()
windows = driver.window_handles
if len(windows) > 1:
    driver.switch_to.window(windows[1])
    driver.close()
    driver.switch_to.window(windows[0])
i = 1
series_name = []
uplo = []
while i <= episode:
    page = requests.get(f"https://e1.lody-net.store/like-flowers-in-sand-ep{i}/")
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    uplo_links = soup.find("div",{"class":"DownloadLinks"}).find("a").attrs['href']
    uplo.append(uplo_links)
    driver.get(uplo_links)
    src = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(src, "lxml")
    name = soup.find("span",{"class":"dfilename"}).text.strip()
    if i == episode:
        csv_name = name
    series_name.append(name)
    soup = BeautifulSoup(src, "lxml")
    try:
        # Wait for the element to be clickable
        download_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.downloadbtn"))
        )
        
        actions = ActionChains(driver)
        actions.move_to_element(download_button).click().perform()
        
        print("Download button clicked successfully.")
    except (ElementClickInterceptedException, TimeoutException):
        print("Download button not clickable or not found")
    i += 1





file_list = [series_name,uplo]
exported = zip_longest(*file_list)
file_path = rf"D:\Projecrs\VS Code\Python\Wep Scraping\lodynet\{csv_name}.csv"
with open(file_path, "w", newline='', encoding='utf-8') as LodyNet:
    wr = csv.writer(LodyNet)
    wr.writerow(["series_name","uplo"])
    wr.writerows(exported)