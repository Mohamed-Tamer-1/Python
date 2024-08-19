from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup WebDriver (ensure you have the correct WebDriver for your browser)
driver = webdriver.Chrome()

# Navigate to the URL
driver.get('https://a120.egyrbyeteuh.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-presumed-innocent-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/')

# Wait for the page to load
time.sleep(5)  # Adjust sleep time as necessary

# Find the download button and click it
download_button = driver.find_element(By.XPATH, "//div[@class='watchNow']//button[@type='submit']")
download_button.click()

# Handle the resulting page or wait for the download to complete
time.sleep(10)  # Adjust sleep time as necessary

# Close the browser
driver.quit()
