from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import json
import os

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://natrue.org/our-standard/natrue-certified-world/?database[tab]=raw-materials")

# Wait for the page to load
time.sleep(1)

# Store scraped data
raw_materials_data = []

# Loop through pagination if necessary
while True:
    # Find all rows in the table
    rows = driver.find_elements(By.CLASS_NAME, "el-table__row")

    # Extract data from each row
    for row in rows:
        try:
            name = row.find_element(By.CLASS_NAME, "el-table_1_column_1").text.strip()
            manufacturer = row.find_element(By.CLASS_NAME, "el-table_1_column_2").text.strip()
            composition = row.find_element(By.CLASS_NAME, "el-table_1_column_3").text.strip()
            inci = row.find_element(By.CLASS_NAME, "el-table_1_column_4").text.strip()
            status = row.find_element(By.CLASS_NAME, "el-table_1_column_5").text.strip()
            expiration = row.find_element(By.CLASS_NAME, "el-table_1_column_6").text.strip()

            # Store the data
            raw_materials_data.append({
                "Name": name,
                "Manufacturer": manufacturer,
                "Composition": composition,
                "INCI": inci,
                "Status": status,
                "Expiration": expiration
            })

            #print(f"✅ Scraped: {name}")

        except Exception as e:
            print(f"⚠️ Error extracting row: {e}")

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

# Convert data to a Pandas DataFrame
df = pd.DataFrame(raw_materials_data)

# Ensure folder exists
os.makedirs("scraped_rawMaterials", exist_ok=True)

# Save data to an Excel file
df.to_excel("scraped_rawMaterials/scraped_rawMaterials.xlsx", index=False)

print("\n🔎 Scraped Data Saved to raw_materials.xlsx")

# Save as JSON
with open("scraped_rawMaterials/scraped_rawMaterials.json", "w", encoding="utf-8") as json_file:
    json.dump(raw_materials_data, json_file, ensure_ascii=False, indent=4)
print("✅ Data saved to `raw_materials.json`")

# Save as CSV
df = pd.DataFrame(raw_materials_data)
df.to_csv("scraped_rawMaterials/scraped_rawMaterials.csv", index=False)
print("✅ Data saved to `raw_materials.csv`")
