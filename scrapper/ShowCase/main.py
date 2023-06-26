import json

from zenrows import ZenRowsClient

from ..loopnet.main import remove_at_symbols


def scrape_showcase(search_type, category, location):
    # try:
        # Perform scraping based on the selected search type and form data
        print("\n\nScraping LoopNet...")
        print(f"Search type: {search_type}")
        print(f"Property name: {category}")
        print(f"Location: {location}\n\n")


        category_mappings = {
            "For Rent": {
                "All Spaces": "commercial-real-estate",
                "Office Space": "office-space",
                "Industrial and Warehouse Space": "warehouses",
                "Retail Space": "retail-space",
                "Restaurants": "restaurants",
                "Flex Space": "flex-space",
                "Medical Offices": "medical-offices",
                "Coworking Space": "coworking-space",
                "Land": "land"
            },
            "For Sale": {
                "All Property Types": "commercial-real-estate",
                "Office Space": "office-space",
                "Industrial Space": "industrial-space",
                "Retail Space": "retail-space",
                "Restaurants": "restaurants",
                "Multifamily Apartments": "apartment-buildings",
                "Hotels & Motels": "hotels",
                "Health Care Properties": "health-care-facilities",
                "Investment Properties": "investment-properties",
                "Land": "land",
                "Shopping Centers & Malls": "shopping-centers-malls",
                "Sports & Entertainment Properties": "sports-entertainment-properties",
                "Residential Income Properties": "residential-income-properties"
            }
        }


        def get_value_by_type_and_key(search_type, key):
            if search_type in category_mappings and key in category_mappings[search_type]:
                return category_mappings[search_type][key]
            else:
                return None


        category_name = get_value_by_type_and_key(search_type, category)
        print(f"Category name: {category_name}")

        # Construct the URL
        if search_type == 'For Sale':
            url = f"https://www.showcase.com/{location}/{category_name}/for-sale/"
        else:
            url = f"https://www.showcase.com/{location}/{category_name}/for-rent/"

        print(f"Scraping {url}...")


        print("Before response...")
        # Make the request with the selected proxy and parameters
        client = ZenRowsClient("e810791d06d06c2bba5a8ee7696f03d65385c0cd")
        # url = "https://www.loopnet.com/"
        params = {"autoparse": "true"}

        response = client.get(url, params=params)

        # print(response.text)
        print("After response...")
        response.raise_for_status()


        json_data = json.loads("".join(response.text))
        modified_data = remove_at_symbols(json_data)

        # print(f"Modified data: {modified_data}...")

        sale_data = [modified_data[0]]

        print(search_type, "search type...")
        url = "https://www.showcase.com"
        listings = []

        if search_type == 'For Rent':
            for key, values in sale_data[0].items():
                if key == 'about':
                    for i in values:
                        # print(f"i: {i}...")
                        listing = {
                            "name": i["item"]["name"],
                            "description": i["item"]["description"],
                            "url": url + i["item"]["url"],
                            "image": i["item"]["image"],
                            "price": i["item"]["price"] + " " + i["item"]["priceCurrency"],
                            "address": i["item"]["availableAtOrFrom"]["address"]["streetAddress"],
                            "locality": i["item"]["availableAtOrFrom"]["address"]["addressLocality"],
                            "region": i["item"]["availableAtOrFrom"]["address"]["addressRegion"],
                        }
                        if listing not in listings:
                            listings.append(listing)
        else:
            for key, values in sale_data[0].items():
                print(f"key: {key}...")
                print(f"values: {values}...")
                if key == 'about':
                    for i in values:
                        # print(f"i: {i}...")
                        listing = {
                            "name": i["item"]["name"],
                            "description": i["item"]["description"],
                            "url": url + i["item"]["url"],
                            "image": i["item"]["image"],
                            "price": i["item"]["price"] + " " + i["item"]["priceCurrency"],
                            "address": i["item"]["availableAtOrFrom"]["address"]["streetAddress"],
                            "locality": i["item"]["availableAtOrFrom"]["address"]["addressLocality"],
                            "region": i["item"]["availableAtOrFrom"]["address"]["addressRegion"],
                        }
                        if listing not in listings:
                            listings.append(listing)




        return listings