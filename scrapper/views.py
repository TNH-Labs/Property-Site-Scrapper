from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    return render(request, 'index.html')

def scrape_loopnet(search_type, property_name, location):
    # Perform scraping based on the selected search type and form data
    url = f"https://www.loopnet.com/{search_type}/"
    params = {
        "location": location,
        "propertyname": property_name
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the desired information from the scraped HTML
    results = []
    listings = soup.find_all('li', class_='placard')
    for listing in listings:
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

    # Return the scraped data
    return results

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

        # Render the search results template with the scraped data
        return render(request, 'search_results.html', {
            'search_type': search_type,
            'property_name': property_name,
            'location': location,
            'scraped_data': scraped_data,
        })

    # Render the search form template for GET requests
    return render(request, 'search.html')
