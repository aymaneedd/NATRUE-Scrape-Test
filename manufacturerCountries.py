import json
import re

# Load Scraped Products Data (to extract brand-manufacturer pairs)
with open("scraped_products/scraped_products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

# Load Scraped Brands Data (to extract country from description)
with open("scraped_brands/scraped_brands.json", "r", encoding="utf-8") as f:
    brands_data = json.load(f)

# Load Countries List
with open("scraped_countries.json", "r", encoding="utf-8") as f:
    country_list = json.load(f)

# Step 1: Extract Unique Manufacturer-Brand Pairs
manufacturer_brand_mapping = {}

for product in products_data:
    manufacturer = product.get("Manufacturer", "").strip()
    brand = product.get("Brand", "").strip()

    if manufacturer and brand:
        manufacturer_brand_mapping[manufacturer] = brand

# 🔹 Print extracted Manufacturer-Brand pairs to check if the mapping is correct
""" print("\n✅ Extracted Manufacturer-Brand Pairs:")
for manufacturer, brand in manufacturer_brand_mapping.items():
    print(f"{manufacturer} → {brand}") """

# Step 2: Extract Country from Brand Descriptions
def extract_country(brand_description):
    lines = brand_description.strip().split("\n")  # Split by line breaks

    #print(f"\n📜 Brand Description:\n{brand_description}")  # Debug: Print full description
    #print(f"🔍 Extracted Lines: {lines}")  # Debug: Show how it's split

    if len(lines) >= 4:
        fourth_line = lines[3].strip()  # Extract fourth line
        #print(f"🟢 Extracted Fourth Line: {fourth_line}")  # Debugging output

        for country in country_list:
            if fourth_line.lower() == country.lower():
                #print(f"✅ Matched Country: {country}")
                return country  # Return the correct country
    return "N/A"

# Step 3: Create Brand-Country Mapping
brand_countries = {}

for brand in brands_data:
    brand_name = brand["Brand Name"].strip()
    brand_description = brand["Description"].strip()
    country = extract_country(brand_description)

    brand_countries[brand_name] = country

# 🔹 Print extracted brand-country mapping for debugging
""" print("\n✅ Extracted Brand-Country Pairs:")
for brand, country in brand_countries.items():
    print(f"{brand} → {country}") """

# Step 4: Assign Country to Each Manufacturer Based on Its Brand
manufacturer_countries = {}

for manufacturer, brand in manufacturer_brand_mapping.items():
    country = brand_countries.get(brand, "N/A")

    # 🔹 Debugging: Print manufacturer-country mapping
    #print(f"✅ Assigning Country: {manufacturer} → {country}")

    manufacturer_countries[manufacturer] = country

# Step 5: Save Cleaned Manufacturer-Country Mapping
with open("manufacturer_countries.json", "w", encoding="utf-8") as f:
    json.dump(manufacturer_countries, f, ensure_ascii=False, indent=4)

print("\n✅ Manufacturer-Country mapping saved successfully!")
