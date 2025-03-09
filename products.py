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
driver.get("https://natrue.org/our-standard/natrue-certified-world/?database[tab]=products")

# Wait for the page to load
time.sleep(1)

# Store scraped data
scraped_products = []

# **Step 1: Scrape Products Without Categories**
while True:
    products = driver.find_elements(By.CLASS_NAME, "product-list__item")
    
    for product in products:
        try:
            name_element = WebDriverWait(product, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-list__item__name"))
            )
            brand_element = WebDriverWait(product, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-list__item__brand"))
            )

            name = name_element.text.strip() if name_element else "N/A"
            brand = brand_element.text.strip() if brand_element else "N/A"

            # Click product to open modal
            driver.execute_script("arguments[0].click();", product)
            time.sleep(0.2)  # Wait for modal

            # Extract details from modal
            try:
                certification = driver.find_element(By.CLASS_NAME, "dialog-product__certification__level").text.strip()
                # Find all elements with the class "dialog-product__info__content"
                info_elements = driver.find_elements(By.CLASS_NAME, "dialog-product__info__content")

                # Ensure there are at least two occurrences before accessing the second one
                if len(info_elements) > 1:
                    manufacturer = info_elements[1].text.strip()  # Get the second occurrence (Manufacturer)
                else:
                    manufacturer = "N/A"  # Fallback if not found
                description = driver.find_element(By.CLASS_NAME, "dialog-product__description").text.strip()
            except:
                certification, manufacturer, description = "N/A", "N/A", "N/A"

            # Close modal
            close_button = driver.find_element(By.CLASS_NAME, "el-icon-close")
            driver.execute_script("arguments[0].click();", close_button)
            time.sleep(0.2)

            # Store the data
            scraped_products.append({
                "Product Name": name,
                "Brand": brand,
                "Certification": certification,
                "Manufacturer": manufacturer,
                "Description": description
            })
        except Exception as e:
            print(f"⚠️ Error extracting product details: {e}")

    # Check if "Next" button exists
    try:
        next_button = driver.find_element(By.CLASS_NAME, "btn-next")
        is_disabled = next_button.get_attribute("disabled")
        if is_disabled:
            print("✅ No more pages. Stopping script.")
            break
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(0.1)
    except:
        print("✅ No more pages. Stopping script.")
        break

# Close the browser
driver.quit()

# Print scraped data
""" print("\n🔎 Final Scraped Products:")
for product in scraped_products:
    print(product)
 """

# Ensure folder exists
os.makedirs("scraped_products", exist_ok=True)

# Save as JSON
with open("scraped_products/scraped_products.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_products, json_file, ensure_ascii=False, indent=4)
print("✅ Data saved to `scraped_products.json`")

# Save as CSV
df = pd.DataFrame(scraped_products)
df.to_csv("scraped_products/scraped_products.csv", index=False)
print("✅ Data saved to `scraped_products.csv`")

