import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

episode = int(input("Enter episodes: "))
name = input("Enter the name of series: ")
name_with_dash = name.replace(" ", "-")
series_name = []
mixdrop = []

for i in range(1, episode + 1):
    url = f"https://eab1.zoool2egpt.shop/%d9%85%d8%b3%d9%84%d8%b3%d9%84-presumed-innocent-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-{i}-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    
    # Find the download link
    down_link = soup.find("a", {"class": "btn download"}).attrs['href']
    
    # Process the download link to find the Mixdrop link
    page = requests.get(down_link)
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    
    # Find all <a> tags with the class "dw"
    mixdrop_links = soup.find_all("a", {"class": "dw"})
    
    # Loop through each <a> tag and check if it contains a <span> with the text "Mixdrop"
    mixdrop_link = None
    for mixdrop_link_tag in mixdrop_links:
        span = mixdrop_link_tag.find("span")
        if span and "megaup" in span.get_text():
            mixdrop_link = mixdrop_link_tag['href']
            mixdrop.append(mixdrop_link)
            series_name.append(f"{name} ep{i}")
            break  # Break once the Mixdrop link is found
    
    if not mixdrop_link:
        print(f"Mixdrop link not found for episode {i}")

file_list = [series_name, mixdrop]
exported = zip_longest(*file_list)
file_path = rf"D:\Projecrs\VS Code\Python\Wep Scraping\CoolCinema\{name}.csv"
with open(file_path, "w", newline='', encoding='utf-8') as CoolCinema:
    wr = csv.writer(CoolCinema)
    wr.writerow(["series_name", "mixdrop"])
    wr.writerows(exported)
