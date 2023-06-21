# views.py
import json
import random
import re

from zenrows import ZenRowsClient
import requests
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

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

def index(request):
    return render(request, 'index.html')

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




import requests
from bs4 import BeautifulSoup

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
            }
        }

        # Get the corresponding category name from the mappings
        category_name = category_mappings[search_type].get(category)
        print(f"Category name: {category_name}\n\n")
        if not category_name:
            if search_type == 'auctions':
                category_name = 'Auctions'
            else:
                return []  # Invalid category

        # Construct the URL
        if search_type == 'forLease':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-lease/"
        elif search_type == 'forSale':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-sale/"
        elif search_type == 'BBSType':
            url = f"https://www.loopnet.com/biz/{location}/{category}/"
        else:
            url = f"https://www.loopnet.com/search/commercial-real-estate/usa/auctions/"

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

        soup = BeautifulSoup(response.content, 'html.parser')


        print("------------------------------------Below is the code where I want desired response--------------------------------------------------")


        listings = []

        listing_elements = soup.select("app-listings-container app-listing-diamond")
        print(f"Found {len(listing_elements)} listings...")
        for element in listing_elements:
            name = element.select_one("h6").text.strip()
            description = element.select_one("p.description").text.strip()
            address = element.select_one(".location").text.strip()
            price = element.select_one(".price").text.strip()

            listing = {
                "name": name,
                "description": description,
                "address": address,
                "price": price
            }
            listings.append(listing)

        # Print the scraped listings
        for listing in listings:
            print(listing)
        print("--------------------------------------------------------------------------------------")




        json_data = json.loads("".join(response.text))
        modified_data = remove_at_symbols(json_data)

        listings = []
        item = modified_data[1]


        if search_type == 'BBSType':
            BBS(modified_data[3])

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

            print(f"\n\nListings:", listings)

        return listings

def BBS(response):
    bbs = response
    print(f"bbs: {bbs}\n\n")
    print("-------------------------------------------end bbs-------------------------------------------")
    for key, value in bbs.items():
            for kii, vii in value.items():
                # print(f"key: {kii}\n\n")
                if kii == 'value':
                    for k, y in vii.items():
                        # print(f"key: {k}\n\n")
                        # print(f"value: {y}\n\n")
                        if k == 'listingAttachments' or k == 'syndicators' or k == 'bfsSearchResult':
                            # print(f"\n\nkey {k}, \nvalue::{y}\n\n")
                            for ke, va in y.items():
                                # print(f"\n\nkey {ke}, \nvalue::{va}\n\n")
                                if ke == 'relatedAuctions':
                                    # print(f"\n\nkey {ke}, \nvalue::{va}\n\n")
                                    for i in va:
                                        for ky, vy in i.items():
                                            if ky == 'listingAttachments':
                                                # print(f"\n\nkey {ky}, \nvalue::{vy}\n\n")
                                                print("---------------first-----------------")
                                                for z in vy:
                                                    for k, v in z.items():
                                                        business = {}
                                                        print(f"\n\nkey {k}, \nvalue::{v}\n\n")




def search_results(request):
    if request.method == 'POST':
        # Access and process the form data here
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forLease':
            property_name = request.POST.get('propertytypeforlease')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')
        elif search_type == 'auction':
            property_name = ''  # Adjust the field name for auctions
        elif search_type == 'BBSType':
            property_name = request.POST.get('propertytypeBBS')
        location = request.POST.get('geography')

        # Perform scraping using the form data
        scraped_data = scrape_loopnet(search_type, property_name, location)

        # print(f"Scraped data: {scraped_data}...")

        # Render the search results template with the scraped data
        return render(request, 'search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': [scraped_data],
        })

    # Render the search form template for GET requests
    return render(request, 'search.html')
