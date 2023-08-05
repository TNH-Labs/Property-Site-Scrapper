import json

from zenrows import ZenRowsClient

from ..loopnet.main import remove_at_symbols


def scrape_showcase(search_type, category, location):
    try:
        # Perform scraping based on the selected search type and form data
        print("\n\nScraping LoopNet...")
        if search_type == 'forSale':
            search_type = 'For Sale'
        else:
            search_type = 'For Rent'




        category_mappings = {
            "For Rent": {
                'All Spaces': 'commercial-real-estate',
                'Office Space': 'office-space',
                'Industrial and Warehouse Space': 'warehouses',
                'Retail Space': 'retail-space',
                'Restaurants': 'restaurants',
                'Flex Space': 'flex-space',
                'Medical Offices': 'medical-offices',
                'Coworking Space': 'coworking-space',
                'Land': 'land',
                'Flex': 'flex-space',
                'Retail': 'retail-space',
                'Special Purpose': 'commercial-real-estate',
                'Hotel and Motel': 'commercial-real-estate',
                'Events': 'commercial-real-estate',
                'Office': 'office-space',
                'Agriculture': 'land',
                'Multi-Family': 'commercial-real-estate',
                'Health Care': 'commercial-real-estate',
                'Restaurant': 'restaurants',
                'Mixed Use': 'commercial-real-estate',
                'Medical': 'medical-offices',
                'Industrial': 'warehouses',
                'Coworking': 'coworking-space',
                'Sports and Entertainment': 'commercial-real-estate',
                'Senior Housing': 'commercial-real-estate'
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
                "Residential Income Properties": "residential-income-properties",
                'Retail': 'retail-space',
                'Mobile Home Park': 'commercial-real-estate',
                'Shopping Center': 'shopping-centers-malls',
                'Note/Loan': 'commercial-real-estate',
                'Restaurant': 'restaurants',
                'Flex Space': 'industrial-space',
                'Multifamily': 'apartment-buildings',
                'Health Care': 'health-care-facilities',
                'Industrial': 'industrial-space',
                'Events': 'commercial-real-estate',
                'Self Storage': 'commercial-real-estate',
                'Hotel and Motel': 'hotels',
                'Residential Income': 'residential-income-properties',
                'Sports & Entertainment': 'sports-entertainment-properties',
                'Senior Housing': 'commercial-real-estate',
                'Mixed Use': 'commercial-real-estate',
                'Agriculture': 'land',
                'Sports and Entertainment': 'sports-entertainment-properties',
                'Hospitality': 'commercial-real-estate',
                'Special Purpose': 'commercial-real-estate',
                'Specialty': 'commercial-real-estate',
                'Multi-Family': 'apartment-buildings',
                'Senior Living': 'commercial-real-estate'
            }

        }


        def get_value_by_type_and_key(search_type, key):
            if search_type in category_mappings and key in category_mappings[search_type]:
                return category_mappings[search_type][key]
            else:
                return None


        category_name = get_value_by_type_and_key(search_type, "Retail Space")

        location = replace_spaces_and_commas(location)
        # Construct the URL
        if search_type == 'forSale':
            url = f"https://www.showcase.com/{location}/{category_name}/for-sale/"
        else:
            url = f"https://www.showcase.com/{location}/{category_name}/for-rent/"
        # Make the request with the selected proxy and parameters
        client = ZenRowsClient("8cb92d04c60beddcb5a5f13c119f96f566525144")
        # url = "https://www.loopnet.com/"
        params = {"autoparse": "true"}

        response = client.get(url, params=params)

        # print(response.text)
        response.raise_for_status()


        json_data = json.loads("".join(response.text))
        modified_data = remove_at_symbols(json_data)

        # print(f"Modified data: {modified_data}...")

        sale_data = [modified_data[0]]

        url = "https://www.showcase.com"
        listings = []

        if search_type == 'For Rent':
            for key, values in sale_data[0].items():
                if key == 'about':
                    # print(f"values: {values}...")
                    for i in values:
                        # print(f"i: {i}...")
                        if i["item"]["availableAtOrFrom"]["address"]["addressLocality"] not in location:
                            print("Not in location...")
                        else:
                            print("In location...")

                        if i["item"]["availableAtOrFrom"]["address"]["addressLocality"] not in location:
                            pass
                        else:
                            try:
                                listing = {
                                    "name": i["item"]["name"],
                                    "description": i["item"]["description"],
                                    "price": i["item"]["price"] + " " + i["item"]["priceCurrency"] if i["item"]["price"] else "Undisclosed",
                                    "address": i["item"]["availableAtOrFrom"]["address"]["streetAddress"],
                                    "locality": i["item"]["availableAtOrFrom"]["address"]["addressLocality"],
                                    "region": i["item"]["availableAtOrFrom"]["address"]["addressRegion"],
                                    "url": url + i["item"]["url"],
                                    "image": i["item"]["image"],
                                }
                            except:
                                listing = {
                                    "name": i["name"],
                                    "description": i["description"],
                                    "price": i["price"] + " " + i["priceCurrency"] if i["price"] else "Undisclosed",
                                    "address": i["availableAtOrFrom"]["address"]["streetAddress"],
                                    "locality": i["availableAtOrFrom"]["address"]["addressLocality"],
                                    "region": i["availableAtOrFrom"]["address"]["addressRegion"],
                                    "url": url + i["url"],
                                    "image": i["image"],
                                }

                            if listing not in listings:
                                listings.append(listing)
        else:
            for key, values in sale_data[0].items():
                if key == 'about':
                    for i in values:
                        if i["item"]["availableAtOrFrom"]["address"]["addressLocality"] not in location:
                            pass
                        else:

                            listing = {
                                "name": i["item"]["name"],
                                "description": i["item"]["description"],
                                "address": i["item"]["availableAtOrFrom"]["address"]["streetAddress"],
                                "locality": i["item"]["availableAtOrFrom"]["address"]["addressLocality"],
                                "region": i["item"]["availableAtOrFrom"]["address"]["addressRegion"],
                                "url": url + i["item"]["url"],
                                "image": i["item"]["image"],
                                # "price": i["item"]["price"] + " " + i["item"]["priceCurrency"],
                            }
                            if listing not in listings:
                                listings.append(listing)



        print(f"Listings showcase: {listings}Listings showcase...\n\n")
        return listings

    except Exception as e:
        print(f"Error: {e}...")
        pass


def replace_spaces_and_commas(string):
    # Split the string into words
    words = string.split()


    # If there are exactly two words
    if len(words) == 2:
        # if there is a comma in the string then remove it
        for i in range(len(words)):
            if "," in words[i]:
                words[i] = words[i].replace(",", "")

        # Reverse the order and join with a slash
        new_string = "/".join(words[::-1])
    elif len(words) > 2:
        # If there are more than two words, last one should go to first with '/' like 'word/' and rest having spaces should replaced with '-' so final string can be 'word/word-word'
        new_string = words[-1] + "/"
        for i in range(len(words) - 1):
            if "," in words[i]:
                words[i] = words[i].replace(",", "")
            new_string += words[i] + "-"
        new_string = new_string[:-1]
    else:
        # If there are more than two words, replace the comma with a dash
        new_string = string.replace(",", "-")

    if new_string[0] == "/":
        # remove it
        new_string = new_string[1] + new_string[2:]

    return new_string
