from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import json
import random
import re
from zenrows import ZenRowsClient

from ..CSV import save_dict_to_csv




def scrape_propertysharks(search_type, category, location):
    # try:
        # Perform scraping based on the selected search type and form data
        print("\n\nScraping propertysharks...")
        print(f"Search type: {search_type}")
        print(f"Property name: {category}")
        print(f"Location: {location}\n\n")
        category_mappings = {
            'Office': 'office',
            'Industrial': 'industrial',
            'Retail': 'retail',
            'Land': 'commercial-real-estate',
            'Flex Space': 'flex-space',
            'Agriculture': 'commercial-real-estate',
            'Hotel and Motel': 'commercial-real-estate',
            'Senior and Housing': 'commercial-real-estate',
            'Health Care': 'commercial-real-estate',
            'Sports and Entertainment': 'commercial-real-estate',
            'Special Purpose': 'commercial-real-estate',
            'Mixed Use': 'commercial-real-estate',
            'Multi-Family': 'commercial-real-estate',
            'Events': 'commercial-real-estate',

        }

        print(f"search_type: {search_type}")
        print(f"cateogry: {category}")

        def get_value_by_type_and_key(search_type, key):
            if search_type in category_mappings and key in category_mappings[search_type]:
                return category_mappings[search_type][key]
            else:
                return None

        category_name = category_mappings[category]


        location = replace_spaces_and_commas(location)

        print(f"category_name: {category_name}")
        print(f"location: {location}")


        # Construct the URL
        url = ""
        if category_name != 'office' or category_name != 'industrial' or category_name != 'retail':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Land':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=4&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name != 'flex-space':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=5&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Agriculture':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=6&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Hotel and Motel':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=7&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Senior and Housing':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=8&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Health Care':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=9&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Sports and Entertainment':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=10&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Special Purpose':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=11&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Mixed Use':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=12&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Multi-Family':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=13&ListingType=Lease&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Events':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=16&ListingType=Lease&CoworkingWorkspaceTypes=0"


        print(f"Scraping {url}...")
        url = replace_spaces_and_commas(url)
        print(f"Scraping {url}...")


        print("Before response...")
        # Make the request with the selected proxy and parameters
        client = ZenRowsClient("e810791d06d06c2bba5a8ee7696f03d65385c0cd")
        params = {"autoparse": "true"}

        response = client.get(url, params=params)

        # print(response.text)
        print("After response...")
        response.raise_for_status()


        json_data = json.loads("".join(response.text))
        modified_data = remove_at_symbols(json_data)


        print(f"modified_data: {modified_data}\n\n")

        # print(f"modified_data: {modified_data}\n\n")

        listings = []
        csv_listings = []
        item = modified_data[1]

        if search_type == 'auctions':
            print("yes it iis auctions")

        # print(f"search_type: {search_type}\n\n")



        if search_type == 'forLease' or search_type == 'forSale':
            if item:
                print(f"item: {item}\n\n")
                for key, value in item.items():
                    # print(f"Key: {key}\n\n")
                    # print(f"Value: {value}\n\n")
                    if key == 'about':
                        print(f"Value: {value}\n\n")
                        try:
                            for i in value:
                                print(f"i: {i}\n\n")
                                for key, value in i['item'].items():
                                    if 'availableAtOrFrom' in i['item']:
                                        if 'address' in i['item']['availableAtOrFrom']:
                                            if 'streetAddress' in i['item']['availableAtOrFrom']['address']:
                                                address = i['item']['availableAtOrFrom']['address']['streetAddress']
                                                locality = i['item']['availableAtOrFrom']['address']['addressLocality']
                                                region = i['item']['availableAtOrFrom']['address']['addressRegion']
                                                # print(f"i val: {address}\n\n")
                                                listing = {
                                                    'name': i['item']['name'],
                                                    'description': i['item']['description'],
                                                    'url': i['item']['url'],
                                                    'image': i['item']['image'],
                                                    'address': address,
                                                    'locality': locality,
                                                    'region': region
                                                }
                                                if listing not in listings:
                                                    listings.append(listing)
                        except:
                            address = value['availableAtOrFrom']['address']['streetAddress']
                            locality = value['availableAtOrFrom']['address']['addressLocality']
                            region = value['availableAtOrFrom']['address']['addressRegion']
                            # print(f"i val: {address}\n\n")
                            listing = {
                                'name': value['name'],
                                'description': value['description'],
                                'url': value['url'],
                                'image': value['image'],
                                'address': address,
                                'locality': locality,
                                'region': region
                            }
                            if listing not in listings:
                                listings.append(listing)


        elif search_type == 'auction':
            if modified_data:
                for item in modified_data:
                    for key, value in item.items():
                        # print(f"Key: {key}\n\n")
                        if key == 'about':
                            # print(f"Value: {value}\n\n")
                            for i in value:
                                # print(f"i: {i}\n\n")
                                for key, value in i['item'].items():
                                    listing = {
                                    'type': i['item']['type'],
                                    'name': i['item']['name'],
                                    'description': i['item']['description'],
                                    'url': i['item']['url'],
                                    'image': i['item']['image'],
                                    'category': i['item']['category'],
                                    'address': i['item']['availableAtOrFrom']['address']['streetAddress'],
                                    'locality': i['item']['availableAtOrFrom']['address']['addressLocality'],
                                    'region': i['item']['availableAtOrFrom']['address']['addressRegion'],
                                    'offered_by': i['item']['offeredBy'][0]['name'],
                                    'offered_by_job_title': i['item']['offeredBy'][0]['jobTitle'],
                                    'works_for': i['item']['offeredBy'][0]['worksFor']['name']
                                    }
                                    if listing not in listings:
                                        listings.append(listing)
        elif search_type == 'BBSType':
            listings = BBS(modified_data[3])

        if listings == [] and search_type == 'forLease' or search_type == 'forSale':
            for key, value in modified_data[2].items():
                # print(f"Key: {key}\n\n")
                # print(f"Value: {value}\n\n")
                if key == 'about':
                    print(f"Value: {value}\n\n")
                    try:
                        for i in value:
                            print(f"i: {i}\n\n")
                            for key, value in i['item'].items():
                                if 'availableAtOrFrom' in i['item']:
                                    if 'address' in i['item']['availableAtOrFrom']:
                                        if 'streetAddress' in i['item']['availableAtOrFrom']['address']:
                                            address = i['item']['availableAtOrFrom']['address']['streetAddress']
                                            locality = i['item']['availableAtOrFrom']['address']['addressLocality']
                                            region = i['item']['availableAtOrFrom']['address']['addressRegion']
                                            # print(f"i val: {address}\n\n")
                                            listing = {
                                                'name': i['item']['name'],
                                                'description': i['item']['description'],
                                                'url': i['item']['url'],
                                                'image': i['item']['image'],
                                                'address': address,
                                                'locality': locality,
                                                'region': region
                                            }
                                            if listing not in listings:
                                                listings.append(listing)
                    except:
                        address = value['availableAtOrFrom']['address']['streetAddress']
                        locality = value['availableAtOrFrom']['address']['addressLocality']
                        region = value['availableAtOrFrom']['address']['addressRegion']
                        # print(f"i val: {address}\n\n")
                        listing = {
                            'name': value['name'],
                            'description': value['description'],
                            'url': value['url'],
                            'image': value['image'],
                            'address': address,
                            'locality': locality,
                            'region': region
                        }
                        if listing not in listings:
                            listings.append(listing)



        return listings

def BBS(response):
    url = "https://www.loopnet.com"
    listings = []
    csv_listings = []
    bbs = response
    print(f"bbs: {bbs}\n\n")
    print(f"url: {url}\n\n")
    # print(f"bbs: {bbs}\n\n")
    print("-------------------------------------------end bbs-------------------------------------------")
    for key, value in bbs.items():
            # print(f"key: {key}\n\n")
            # print(f"value: {value}\n\n")
            if key == 'csr':
                for i in value:

                    # for kii, vii in i.items():
                    # print(f"vii: {vii}\n\n")
                    # print(f"kii: {kii}\n\n")
                    try:
                        listing = {
                            'url':url + i['urlStub'],
                            'listNumber': i['listNumber'],
                            'header': i['header'],
                            'description': i['description'],
                            'price': i['price'],
                            'image': url + i['img'][0],
                            'location': i['location'],
                            'cashFlow': i['cashFlow'],
                            'Contact_name': i['contactInfo']['contactFullName'],
                            'Contact_phone': i['contactInfo']['contactPhoneNumber']['telephone']
                        }
                    except:
                        listing = {
                            'url': url + i['urlStub'],
                            'listNumber': i['listNumber'],
                            'header': i['header'],
                            'description': i['description'],
                            'price': i['price'],
                            'image': url + i['img'][0],
                            'location': i['location'],

                        }

                    if listing not in listings:
                        listings.append(listing)


    # print(f"\n\nListings:", listings)
    return listings

def remove_at_symbols(obj):
    if isinstance(obj, dict):
        modified_obj = {}
        for key, value in obj.items():
            modified_key = key.replace("@", "")
            modified_value = remove_at_symbols(value)
            modified_obj[modified_key] = modified_value
        return modified_obj
    elif isinstance(obj, list):
        modified_obj = []
        for item in obj:
            modified_item = remove_at_symbols(item)
            modified_obj.append(modified_item)
        return modified_obj
    else:
        return obj


def find_value(data, target):
    if isinstance(data, dict):
        for key, value in data.items():
            if value == target:
                return value
            elif isinstance(value, (dict, list)):
                result = find_value(value, target)
                if result:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_value(item, target)
            if result:
                return result

    return None

def replace_spaces_and_commas(string):
    # Split the string into words
    words = string.split()

    # If there are exactly two words
    if len(words) == 2:
        # Reverse the order and join with a slash
        new_string = "/".join(words[::-1])
    else:
        # If there are more than two words, replace the comma with a dash
        new_string = string.replace(",", "-")

    if new_string[0] == "/":
        print(f"new stirng = {new_string}")
        # remove it
        new_string = new_string[1] + new_string[2:]

    print(f"new stirng = {new_string}")

    return new_string
