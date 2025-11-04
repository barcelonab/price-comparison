import requests
import pandas as pd
import time

# 🔐 Zyla Labs API configuration
api_key = "10972|2WcPHKmatQaR3oDmx6GJAQEbGFmLt0ASDfvkBk6s"
base_url = "https://zylalabs.com/api/2332/prices+comparison+api/14550/get+comparison"
country = "us"

# 🛍️ List of products to search
products = ["A430i", "A660i", "A790i", "E1060i", "E1060s", "E660i", "E790i"]

# Store all products in a single list
all_results = []

for product in products:
    print(f"\n🔍 Fetching results for: {product}")
    page = 1

    while True:
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
columns_to_keep = ["model", "title", "source", "price", "imageUrl","link"]
df = df[[col for col in columns_to_keep if col in df.columns]]

# Save to CSV
if not df.empty:
    file_name = r"D:\Reports\Power BI\Price Comparison\zyla_all_products.csv"
    df.to_csv(file_name, index=False)
    print(f"\n✅ Saved {len(df)} total items to '{file_name}'")
else:
    print("\n⚠️ No data returned from the API.")