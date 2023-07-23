# views.py
import csv
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .ShowCase.main import scrape_showcase
from .crexi.main import scrape_crexi
from .loopnet.main import *
from .propertysharks.main import scrape_propertysharks
from concurrent.futures import ThreadPoolExecutor, as_completed
global scraped_data

state_abbreviations = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"
    }

def index(request):
    return render(request, 'index.html')


def convert_to_full_state_name(abbreviation):
    return state_abbreviations.get(abbreviation.upper(), abbreviation).title()


def Csv(request):
    data = request.session['scrapdata']
    updated_data = []
    for i in data:
        updated_dict = {}
        for key, value in i.items():
            # if key != 'image' and key != 'url' and key != 'image_url' and key != 'img_url' or key != 'href' or key != 'src':
            if key == 'name' or key == 'description' or key == 'price' or key == 'address' or key == 'locality' or key == 'region' or key == 'title':
                if key == 'region' and len(value.strip(" ")) == 2:
                    full_name = convert_to_full_state_name(value.strip(" "))
                    updated_dict[key] = full_name
                elif key == 'region' and value not in state_abbreviations.values() or len(value) == 0 or value == ' ':
                   pass
                else:
                    updated_dict[key] = value.strip(" ")

        updated_data.append(updated_dict)
    keys = updated_data[0].keys()
    response = HttpResponse(content_type='text/csv')
    name = request.session['name']
    response['Content-Disposition'] = f'attachment; filename="{name}.csv"'
    writer = csv.writer(response)
    writer.writerow(keys)  # add header row
    for row in updated_data:
        writer.writerow(row.values())
    return response


def loopnet(request):
    if request.method == 'POST':
        # Access and process the form data here
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forLease':
            property_name = request.POST.get('propertytypeforlease')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')
        elif search_type == 'auction':
            property_name = 'auction'  # Adjust the field name for auctions
        elif search_type == 'BBSType':
            property_name = request.POST.get('propertytypeBBS')
        location = request.POST.get('geography')

        # Perform scraping using the form data
        scraped_data = scrape_loopnet(search_type, property_name, location)
        print(f"Scraped data: {scraped_data}...")

        request.session['scrapdata'] = scraped_data
        request.session['name'] = location

        if search_type == 'BBSType':
            return render(request, 'Loopnet/BBS.html', {
                'listings': scraped_data
            })
        elif search_type == 'aunctions':
            return render(request, 'Loopnet/auctions.html', {
                'listings': scraped_data
            })
        else:
            return render(request, 'Loopnet/search_results.html', {
                'search_type': search_type,
                'property_name': property_name,
                'location': location,
                'scraped_data': [scraped_data],
            })

    # Render the search form template for GET requests
    return render(request, 'Loopnet/search.html')


def showcase(request):
    if request.method == 'POST':
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forLease':
            property_name = request.POST.get('propertytypeforrent')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')

        print(property_name, "property_name")

        location = request.POST.get('geography')

        scraped_data = scrape_showcase(search_type, property_name, location)
        request.session['scrapdata'] = scraped_data
        request.session['name'] = location

        return render(request, 'ShowCase/search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': [scraped_data],
        })



    return render(request, 'ShowCase/search.html')

def crexi(request):
    if request.method == 'POST':
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forLease':
            property_name = request.POST.get('propertytypeforlease')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')
        elif search_type == 'auction':
            property_name = request.POST.get('propertytypebbs')

        location = request.POST.get('geography')

        scraped_data = scrape_crexi(location, property_name, search_type)
        request.session['scrapdata'] = scraped_data
        request.session['name'] = location


        return render(request, 'crexi/search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': [scraped_data],
        })

    return render(request, 'crexi/search.html')

def propertysharks(request):
    if request.method == 'POST':
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forRent':
            property_name = request.POST.get('propertytypeforrent')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')

        location = request.POST.get('geography')

        print(location, "location")
        print(property_name, "property_name")
        print(search_type, "search_type")

        scraped_data = scrape_propertysharks(search_type, property_name, location)
        request.session['scrapdata'] = scraped_data
        request.session['name'] = location

        return render(request, 'propertysharks/search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': [scraped_data],
        })

    return render(request, 'propertysharks/search.html')


def search(request):
    if request.method == 'POST':
        # Access and process the form data here
        search_type = request.POST.get('search-type')
        property_name = None
        if search_type == 'forLease' or search_type == 'forRent':
            property_name = request.POST.get('propertytypeforlease')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')
        elif search_type == 'auction':
            property_name = 'auction'  # Adjust the field name for auctions
        elif search_type == 'BBSType':
            property_name = request.POST.get('propertytypeBBS')
        location = request.POST.get('geography')

        print(property_name, "property_name")

        # Perform scraping using the form data
        if search_type == 'forLease' or search_type == 'forSale' or search_type == 'forRent':
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(scrape_loopnet, search_type, property_name, location),
                           executor.submit(scrape_showcase, search_type, property_name, location),
                           executor.submit(scrape_propertysharks, search_type, property_name, location),
                           executor.submit(scrape_crexi, location, property_name, search_type)]

                scraped_data = []
                for future in as_completed(futures):
                    result = future.result()
                    try:
                        scraped_data += result
                    except:
                        pass
        elif search_type == 'auction':
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(scrape_loopnet, search_type, property_name, location),
                           executor.submit(scrape_crexi, location, property_name, search_type)]

                scraped_data = []
                for future in as_completed(futures):
                    result = future.result()
                    try:
                        scraped_data += result
                    except:
                        pass
        else:
            with ThreadPoolExecutor() as executor:
                scraped_data = executor.submit(scrape_loopnet, search_type, property_name, location).result()

        # print(f"Scraped data: {scraped_data}...")

        request.session['scrapdata'] = scraped_data
        request.session['name'] = location

        if search_type == 'BBSType':
            return render(request, 'BBS.html', {
                'listings': scraped_data
            })
        elif search_type == 'auctions':
            return render(request, 'auctions.html', {
                'listings': scraped_data
            })
        else:
            return render(request, 'search_results.html', {
                'search_type': search_type,
                'property_name': property_name,
                'location': location,
                'scraped_data': [scraped_data],
            })

    # Render the search form template for GET requests
    return render(request, 'search.html')





