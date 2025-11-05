import requests
import pandas as pd
import time
from datetime import datetime

# 🔐 Zyla Labs API configuration
api_key = "11044|6I98ta7GgDvnB6ESRpGfUZWoxkpDl9cWP5t21vMd"
base_url = "https://zylalabs.com/api/7604/price+compare+api/14551/get+comparison"
country = "us"

# 🛍️ List of products to search
products = ["A790i-8EAN","A790i-8LAN","A660i-8EAN","A660i-8LAN"]

# Store all products in a single list
all_results = []

for product in products:
    print(f"\n🔍 Fetching results for: {product}")
    page = 1

    while page <= 1:
        print(f"  📄 Page {page}...")
        response = requests.get(
            base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            params={"query": product, "page": page, "country": country}
        )

        if response.status_code != 200:
            print(f"  ⚠️ Error {response.status_code}")
            break

        data = response.json()
        products_data = data.get("products", [])

        if not products_data:
            print(f"  ✅ No more pages for {product}.")
            break

        # Add search term and page number for traceability
        for item in products_data:
            item["model"] = product
            

        all_results.extend(products_data)
        page += 1

        # Wait 1 second between requests (Zyla limit = 60/min)
        time.sleep(1)

# ✅ Convert all results to DataFrame
df = pd.DataFrame(all_results)

# Keep only specific columns (rename if necessary)
columns_to_keep = ["model", "title", "source", "price", "imageUrl", "link"]
df = df[[col for col in columns_to_keep if col in df.columns]]

# 🕒 Add current date and time
df["datetime_fetched"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save to CSV
if not df.empty:
    file_name = r"D:\Reports\Power BI\Price Comparison\zyla_all_products.csv"
    df.to_csv(file_name, index=False)
    print(f"\n✅ Saved {len(df)} total items to '{file_name}'")
else:
    print("\n⚠️ No data returned from the API.")