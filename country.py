import pandas as pd
from geopy.geocoders import Nominatim
import time

file_path = "Source 2/pokemon_championships.csv"

print("Loading CSV file...")
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower()

geolocator = Nominatim(user_agent="dv2_pokemon_mapper")
coord_map = {}

unique_locations = df[["city", "country"]].drop_duplicates()
total = len(unique_locations)
print(f"Found {total} unique locations. Starting coordinate lookup...\n")

# Fetch coordinates with live console logging
for _, row in unique_locations.iterrows():
    city = str(row["city"]).strip()
    country = str(row["country"]).strip()
    query = f"{city}, {country}"

    print(f"Searching for {query}... ", end="")

    try:
        loc = geolocator.geocode(query, timeout=10)
        if loc:
            coord_map[(city, country)] = (loc.latitude, loc.longitude)
            print(f"FOUND: {loc.latitude}, {loc.longitude}")
        else:
            coord_map[(city, country)] = (None, None)
            print("NOT FOUND")
    except Exception as e:
        coord_map[(city, country)] = (None, None)
        print(f"ERROR: {e}")

    time.sleep(1.5)  # 1.5 seconds ensures we don't get blocked by the API

print("\nApplying coordinates to the spreadsheet...")
df["latitude"] = df.apply(
    lambda r: coord_map.get(
        (str(r["city"]).strip(), str(r["country"]).strip()), (None, None)
    )[0],
    axis=1,
)
df["longitude"] = df.apply(
    lambda r: coord_map.get(
        (str(r["city"]).strip(), str(r["country"]).strip()), (None, None)
    )[1],
    axis=1,
)

df.to_csv(file_path, index=False)
print(f"Done! Saved back to {file_path}")
