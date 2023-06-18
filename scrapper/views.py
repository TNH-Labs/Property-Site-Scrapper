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
            'BBSType': {}  # No options for Auctions
        }

        # Get the corresponding category name from the mappings
        category_name = category_mappings[search_type].get(category)
        if not category_name:
            return []  # Invalid category

        # Construct the URL
        url = ""
        if search_type == 'forLease':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-lease/"
        elif search_type == 'forSale':
            url = f"https://www.loopnet.com/search/{category}/{location}/for-sale/"
        elif search_type == 'BBSType':
            url = f"https://www.loopnet.com/biz/{location}/{category}/"

        print(f"Scraping {url}...")

        # Define the proxy URL
        proxy_url = 'https://proxy-server.scraperapi.com:8001'

        # Set the request parameters
        params = {
            'api_key': '6e5709e72aca3705fd3914be2e16c635',
            'autoparse': 'true'
        }

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


        # print(f"soup {soup}...\n\n")

        print("Scraping mid3!")

        # Extract the desired information from the scraped HTML
        results = []
        listings = soup.find_all('li', class_='placard')
        print(listings)
        print("Scraping mid3!")
        for listing in listings:
            print("Scraping mid4!")
            title = listing.find('h2', class_='listing-title').text.strip()
            address = listing.find('div', class_='placard-header').text.strip()
            url = listing.find('a', class_='placard-titleLink').get('href')
            price = listing.find('span', class_='price').text.strip()
            details = listing.find('ul', class_='details').text.strip()
            result = {
                'title': title,
                'address': address,
                'url': url,
                'price': price,
                'details': details
            }
            results.append(result)

        print(f"Scraped {len(results)} results from LoopNet.")

        # print(f"Results:",response.text.strip().split('\n'))

        json_data = json.loads("".join(response.text))

        modified_data = remove_at_symbols(json_data)

        # Extract the property listings
        listings = []
        item = modified_data[1]
        # print(f"data: {data}")
        if item:
            # print(f"item: {item}")
            for key, value in item.items():
                # print(f"key: {key}, value: {value}")
                if key == 'about':
                    for i in value:
                        # print(f"i: {i}")
                        if i['item']:
                            # print(f"i['item']: {i['item']}")
                            for key, value in i['item'].items():
                                print(f"key: {key}, value: {value}")
                                listing = {
                                    'name': i['item']['name'],
                                    'description': i['item']['description'],
                                    'url': i['item']['url'],
                                    'image': i['item']['image'],
                                    'address': i['item']['availableAtOrFrom']['address']['streetAddress'],
                                    'locality': i['item']['availableAtOrFrom']['address']['addressLocality'],
                                    'region': i['item']['availableAtOrFrom']['address']['addressRegion']
                                }
                                listings.append(listing)
                                print("\n\n\n yes \n\n\n")

            # if isinstance(item, dict) and item.get('type') == 'Offer':
            #     listing = {
            #         'name': item['name'],
            #         'description': item['description'],
            #         'url': item['url'],
            #         'image': item['image'],
            #         'address': item['availableAtOrFrom']['address']['streetAddress'],
            #         'locality': item['availableAtOrFrom']['address']['addressLocality'],
            #         'region': item['availableAtOrFrom']['address']['addressRegion']
            #     }
            #     listings.append(listing)

        # Print the property listings
        print(f"\n\nListings:", listings)
        # for listing in listings:
        #     print(listing)

        # # Remove the "@" symbol from keys in each dictionary
        # modified_data = []
        # for item in json_data:
        #     modified_item = {}
        #     for key, value in item.items():
        #         modified_key = key.replace("@", "")
        #         modified_item[modified_key] = value
        #     modified_data.append(modified_item)
        #
        # print(f"\n\nModified data: {modified_dat}...")
        #
        # cleaned_data = {}
        # for i in response.text.strip().split('\n'):
        #     print(f"i: {i}...")
        #     for key, value in i:
        #         cleaned_key = re.sub('^@', '', key)
        #         cleaned_data[cleaned_key] = value
        #
        #
        # print(f"Cleaned data: {cleaned_data}...")

        return modified_data

    # except Exception as e:
    #     print(f"An error occurred during scraping: {str(e)}")
    #     return []


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
