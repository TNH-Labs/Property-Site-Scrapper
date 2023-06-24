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
                'coworking-space': 'Coworking',
                'industrial-space': 'Industrial',
                'retail-space': 'Retail',
                'restaurants': 'Restaurant',
                'flex-space': 'Flex',
                'medical-offices': 'Medical',
                'land': 'Land',
            },
            'forSale': {
                'office-buildings': 'Office',
                'industrial-properties': 'Industrial',
                'retail-properties': 'Retail',
                'restaurants': 'Restaurant',
                'shopping-centers': 'Shopping Center',
                'apartment-buildings': 'Multifamily',
                'commercial-real-estate': 'Specialty',
                'health-care-facilities': 'Health Care',
                'hospitality-properties': 'Hospitality',
                'sports-entertainment-properties': 'Sports & Entertainment',
                'land': 'Land',
                'residential-income-properties': 'Residential Income',
            },
            'BBSType': {
                'restaurants-and-food-businesses-for-sale': 'Restaurants & Food',
                'retail-businesses-for-sale': 'Retail',
                'service-businesses-for-sale': 'Service Businesses',
                'wholesale-and-distribution-businesses-for-sale': 'Wholesale & Distributors',
                'transportation-and-storage-businesses-for-sale': 'Transportation & Storage',
                'online-and-technology-businesses-for-sale': 'Online & Technology',
                'automotive-and-boat-businesses-for-sale': 'Automotive & Boat',
                'franchises-for-sale': 'Franchise Opportunities',
                'california-businesses-for-sale': 'All Industries'
            },
            'auctions': {}
        }

        # Get the corresponding category name from the mappings
        try:
            category_name = category_mappings[search_type].get(category)
        except:
            category_name = 'auctions'
        print(f"Category name: {category_name}\n\n")

        # Construct the URL
        if search_type == 'forLease':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-lease/"
        elif search_type == 'forSale':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-sale/"
        elif search_type == 'BBSType':
            url = f"https://www.loopnet.com/biz/{location}/{category}/"
        else:
            url = f"https://www.loopnet.com/search/commercial-real-estate/{location.lower()}/auctions/"

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

        print(f"modified_data: {modified_data}\n\n")

        listings = []
        csv_listings = []
        item = modified_data[1]

        if search_type == 'auctions':
            print("yes it iis auctions")

        print(f"search_type: {search_type}\n\n")



        if search_type == 'forLease' or search_type == 'forSale':
            if item:
                for key, value in item.items():
                    if key == 'about':
                        # print(f"Value: {value}\n\n")
                        for i in value:
                            print(f"i: {i}\n\n")
                            for key, value in i['item'].items():
                                if 'availableAtOrFrom' in i['item']:
                                    if 'address' in i['item']['availableAtOrFrom']:
                                        if 'streetAddress' in i['item']['availableAtOrFrom']['address']:
                                            address = i['item']['availableAtOrFrom']['address']['streetAddress']
                                            locality = i['item']['availableAtOrFrom']['address']['addressLocality']
                                            region = i['item']['availableAtOrFrom']['address']['addressRegion']
                                            print(f"i val: {address}\n\n")
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

        elif search_type == 'auction':
            if modified_data:
                for item in modified_data:
                    for key, value in item.items():
                        print(f"Key: {key}\n\n")
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


        return listings

def BBS(response):
    url = "https://www.loopnet.com"
    listings = []
    csv_listings = []
    bbs = response
    print(f"url: {url}\n\n")
    # print(f"bbs: {bbs}\n\n")
    print("-------------------------------------------end bbs-------------------------------------------")
    for key, value in bbs.items():
            # print(f"key: {key}\n\n")
            # print(f"value: {value}\n\n")
            if key == 'csr':
                for i in value:
                    # print(f"i: {i}\n\n")
                    # for kii, vii in i.items():
                    # print(f"vii: {vii}\n\n")
                    # print(f"kii: {kii}\n\n")
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
                    if listing not in listings:
                        listings.append(listing)
                        csv_listings.append(csv)



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
