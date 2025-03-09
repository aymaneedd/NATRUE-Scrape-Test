from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd
import os

# Set up the Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://natrue.org/our-standard/natrue-certified-world/?database[tab]=brands")

# Wait for the page to load
time.sleep(1)

try:
    # Find element with the class "el-select"
    dropdowns = driver.find_elements(By.CLASS_NAME, "el-select")
    # Click the dropdown
    driver.execute_script("arguments[0].click();", dropdowns[0])
    time.sleep(1)

    # Find all country items
    country_list = driver.find_elements(By.CLASS_NAME, "el-select-dropdown__item")

    # Extract country names
    countries = [cat.text.strip() for cat in country_list if cat.text.strip()]

    """ print("✅ Countries Found:")
    for country in countries:
        print(country) """

except Exception as e:
    print(f"❌ Error extracting countries: {e}")

# Ensure folder exists
os.makedirs("scraped_countries", exist_ok=True)

# Save as JSON
with open("scraped_countries.json", "w", encoding="utf-8") as json_file:
    json.dump(countries, json_file, ensure_ascii=False, indent=4)
print("✅ Data saved to `scraped_brands.json`")