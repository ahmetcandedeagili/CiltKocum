import os
import glob
import pandas as pd
import kagglehub

# get the sephora dataset
print("downloading sephora data...")
sephora_path = kagglehub.dataset_download("nadyinky/sephora-products-and-skincare-reviews")

# path to the csv
sephora_csv = os.path.join(sephora_path, 'product_info.csv')
df_products = pd.read_csv(sephora_csv)

# columns we care about
cols = [
    'product_id', 'product_name', 'brand_name', 'loves_count', 
    'rating', 'price_usd', 'primary_category', 'secondary_category',
    'ingredients'
]

# filter the dataframe and get only skincare
df_clean = df_products[cols]
df_skincare = df_clean[df_clean['primary_category'] == 'Skincare']

# save to a new csv
df_skincare.to_csv('sephora_skincare_products.csv', index=False)
print("saved sephora data")

# now get the inci dataset
print("downloading inci data...")
inci_path = kagglehub.dataset_download("amaboh/skin-care-product-ingredients-inci-list")

# use glob to find the csv inside the downloaded folder
inci_files = glob.glob(os.path.join(inci_path, "*.csv"))

if inci_files:
    inci_csv = inci_files[0] # grab the first csv it finds
    df_inci = pd.read_csv(inci_csv)

    # we don't need the url column, drop it if it exists
    if 'url' in df_inci.columns:
        df_inci = df_inci.drop(columns=['url'])
        
    # save the cleaned inci data
    df_inci.to_csv('inci_ingredients_cleaned.csv', index=False)
    print("saved inci data")
else:
    print("error: csv file not found for inci data")

print("all done!")