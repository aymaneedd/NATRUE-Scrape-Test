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

# **Step 1: Scrape All Brands Details**
scraped_brands = []
while True:
    # Find all brand containers
    brands = driver.find_elements(By.CLASS_NAME, "brand-list__item")

    # Extract brand details
    for brand in brands:
        try:
            name_element = WebDriverWait(brand, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "brand-list__item__name"))
            )

            name = name_element.text.strip() if name_element else "N/A"

            # Scroll brand into view before clicking
            driver.execute_script("arguments[0].scrollIntoView();", brand)
            time.sleep(0.1)

            # Click brand using JavaScript to ensure it works
            driver.execute_script("arguments[0].click();", brand)
            time.sleep(0.1)  # Wait for the modal to open

            # Extract details from modal
            try:
                description = driver.find_element(By.CLASS_NAME, "dialog-brand__description").text.strip()
            except:
                description = "N/A"

            # Close the modal
            close_button = driver.find_element(By.CLASS_NAME, "el-icon-close")
            close_button.click()
            time.sleep(0.1)

            # Store the data
            scraped_brands.append({
                "Brand Name": name,
                "Description": description
            })

        except Exception as e:
            print(f"⚠️ Error extracting brand details: {e}")

    # **Step 1: Check if the "Next" button exists**
    try:
        next_button = driver.find_element(By.CLASS_NAME, "btn-next")

        # **Step 2: Check if the "Next" button is disabled**
        is_disabled = next_button.get_attribute("disabled")
        if is_disabled:
            print("✅ No more pages. Stopping the script.")
            break  # Exit loop when the next button is disabled

        # **Step 3: Click the "Next" button**
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(0.2)  # Wait for new rows to load

    except:
        print("✅ No more pages. Stopping the script.")
        break  # Exit loop when no next button is found

# Close the browser
driver.quit()

""" # Print the final scraped data
print("\n🔎 Final Scraped Products:")
for brand in scraped_brands:
    print(brand)
 """
# Ensure folder exists
os.makedirs("scraped_brands", exist_ok=True)

# Save as JSON
with open("scraped_brands/scraped_brands.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_brands, json_file, ensure_ascii=False, indent=4)
print("✅ Data saved to `scraped_brands.json`")

# Save as CSV
df = pd.DataFrame(scraped_brands)
df.to_csv("scraped_brands/scraped_brands.csv", index=False)
print("✅ Data saved to `scraped_brands.csv`")