# views.py
import csv

import requests
from django.http import HttpResponse
from django.shortcuts import render

from .CSV import save_dict_to_csv
from .ShowCase.main import scrape_showcase
from .loopnet.main import *

global scraped_data


def index(request):
    return render(request, 'index.html')


def csv_loopnet(request):
    data = request.session['scrapdata']
    updated_data = []
    for i in data:
        updated_dict = {}
        for key, value in i.items():
            if key != 'image' and key != 'url':
                updated_dict[key] = value
        updated_data.append(updated_dict)
    keys = updated_data[0].keys()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'
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

        request.session['scrapdata'] = scraped_data

        # print(f"Scraped data: {scraped_data}...")

        # Render the search results template with the scraped data
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

        location = request.POST.get('geography')

        scraped_data = scrape_showcase(search_type, property_name, location)
        request.session['scrapdata'] = scraped_data
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
            property_name = request.POST.get('propertytypeforrent')
        elif search_type == 'forSale':
            property_name = request.POST.get('propertytypeforsale')

        location = request.POST.get('geography')


        return render(request, 'Crexi/search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': [scraped_data],
        })

    return render(request, 'Crexi/search.html')

