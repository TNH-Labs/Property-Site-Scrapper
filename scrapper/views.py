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


def index(request):
    return render(request, 'index.html')


def Csv(request):
    data = request.session['scrapdata']
    updated_data = []
    for i in data:
        updated_dict = {}
        for key, value in i.items():
            if key != 'image' and key != 'url' and key != 'image_url' and key != 'img_url':
                updated_dict[key] = value
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
        if search_type == 'forLease' or search_type == 'forSale':
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
        elif search_type == 'auction' or search_type == 'forSale' or search_type == 'forLease':
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

        print(f"Scraped data: {scraped_data}...")

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


