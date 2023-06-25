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
                "commercial-real-estate": "All Spaces",
                "office-space": "Office Space",
                "warehouses": "Industrial and Warehouse Space",
                "retail-space": "Retail Space",
                "restaurants": "Restaurants",
                "flex-space": "Flex Space",
                "medical-offices": "Medical Offices",
                "coworking-space": "Coworking Space",
                "land": "Land"
            },
            "For Sale": {
                "commercial-real-estate": "All Property Types",
                "office-space": "Office Space",
                "industrial-space": "Industrial Space",
                "retail-space": "Retail Space",
                "restaurants": "Restaurants",
                "apartment-buildings": "Multifamily Apartments",
                "hotels": "Hotels & Motels",
                "health-care-facilities": "Health Care Properties",
                "investment-properties": "Investment Properties",
                "land": "Land",
                "shopping-centers-malls": "Shopping Centers & Malls",
                "sports-entertainment-properties": "Sports & Entertainment Properties",
                "residential-income-properties": "Residential Income Properties"
            }
        }


        category_name = category_mappings[search_type].get("land")
        print(f"Category name: {category_name}")

        # Construct the URL
        if search_type == 'For Sale':
            url = f"https://www.showcase.com/{location}/{category}/for-sale/"
        else:
            url = f"https://www.showcase.com/{location}/{category}/for-rent/"

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

        if search_type == 'For Sale':
            for key, values in sale_data[0].items():
                print(f"Key: {key}...")
                print(f"Values: {values}...")
                if key == 'about':
                    print("yes")
                # if key == "breadcrumb":
                #     for value in values:
                #         for kii, vii in value.items():
                #             if kii == ['itemListElement']:
                #                 for i in vii:
                #                     for k,v in i:



        return modified_data