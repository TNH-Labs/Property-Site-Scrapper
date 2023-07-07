from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import json
import random
import re
from zenrows import ZenRowsClient

from ..CSV import save_dict_to_csv




def scrape_loopnet(search_type, category, location):
    # try:
        # Perform scraping based on the selected search type and form data
        print("\n\nScraping LoopNet...")
        print(f"Search type: {search_type}")
        print(f"Property name: {category}")
        print(f"Location: {location}\n\n")
        category_mappings = {
            'forLease': {
                'Coworking': 'coworking-space',
                'Industrial': 'industrial-space',
                'Retail': 'retail-space',
                'Restaurant': 'restaurants',
                'Flex': 'flex-space',
                'Medical': 'medical-offices',
                'Land': 'land'
            },
            'forSale': {
                'Office': 'office-buildings',
                'Industrial': 'industrial-properties',
                'Retail': 'retail-properties',
                'Restaurant': 'restaurants',
                'Shopping Center': 'shopping-centers',
                'Multifamily': 'apartment-buildings',
                'Specialty': 'commercial-real-estate',
                'Health Care': 'health-care-facilities',
                'Hospitality': 'hospitality-properties',
                'Sports & Entertainment': 'sports-entertainment-properties',
                'Land': 'land',
                'Residential Income': 'residential-income-properties'
            },
            'BBSType': {
                'Restaurants & Food': 'restaurants-and-food-businesses-for-sale',
                'Retail': 'retail-businesses-for-sale',
                'Service Businesses': 'service-businesses-for-sale',
                'Wholesale & Distributors': 'wholesale-and-distribution-businesses-for-sale',
                'Transportation & Storage': 'transportation-and-storage-businesses-for-sale',
                'Online & Technology': 'online-and-technology-businesses-for-sale',
                'Automotive & Boat': 'automotive-and-boat-businesses-for-sale',
                'Franchise Opportunities': 'franchises-for-sale',
                'All Industries': 'california-businesses-for-sale'
            },
            'auctions': {}
        }

        print(f"search_type: {search_type}")
        print(f"cateogry: {category}")

        def get_value_by_type_and_key(search_type, key):
            if search_type in category_mappings and key in category_mappings[search_type]:
                return category_mappings[search_type][key]
            else:
                return None

        category_name = get_value_by_type_and_key(search_type, category)


        # Construct the URL
        if search_type == 'forLease':
            url = f"https://www.loopnet.com/search/{category_name}/{location}/for-lease/"
        elif search_type == 'forSale':
            url = f"https://www.loopnet.com/search/{category_name}/{location}/for-sale/"
        elif search_type == 'BBSType':
            url = f"https://www.loopnet.com/biz/{location}/{category_name}/"
        else:
            url = f"https://www.loopnet.com/search/commercial-real-estate/{location.lower()}/auctions/"

        print(f"Scraping {url}...")
        url = replace_spaces_and_commas(url)
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

        print(f"modified_data: {modified_data[2]}\n\n")

        # print(f"modified_data: {modified_data}\n\n")

        listings = []
        csv_listings = []
        item = modified_data[1]

        if search_type == 'auctions':
            print("yes it iis auctions")

        print(f"search_type: {search_type}\n\n")



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
    # Replace spaces with dashes
    string = string.replace(" ", "-")
    # Replace commas with dashes
    string = string.replace(",", "-")
    return string
