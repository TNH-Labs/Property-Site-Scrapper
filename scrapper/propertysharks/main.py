import ast

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import json
import random
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from zenrows import ZenRowsClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui as pg

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

        # print(f"response: {response}\n\n")
        # print(f"response.text: {response.text}\n\n")

        # print(response.text)
        print("After response...")
        response.raise_for_status()


        json_data = json.loads("".join(response.text))
        modified_data = remove_at_symbols(json_data)


        # print(f"modified_data: {modified_data}\n\n")

        # print(f"modified_data: {modified_data}\n\n")

        listings = []
        csv_listings = []
        item = modified_data[1]

        if search_type == 'auctions':
            print("yes it iis auctions")

        # print(f"search_type: {search_type}\n\n")


        option = Options()
        # option.add_argument("--window-size=1920,1080")
        option.add_argument("--start-maximized")
        # option.add_argument("--headless")
        # option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        option.add_argument("--disable-notifications")
        option.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome("./chromedriver.exe", options=option)

        # driver = webdriver.Chrome(options=option, service=service_)
        # driver.set_window_rect(width=1500, height=1000)
        xpath = "//div//ul[@class='listings']"
        # try:
        # print("url: ",url)
        driver.get(url)
        # listing_element = driver.find_element(By.XPATH, all )
        wait = WebDriverWait(driver, 15)
        listing_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        # print(f"Found {listing_element} listing element")


        def scroll_to_element(driver, element):
            # driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
            viewport_height = driver.execute_script("return window.innerHeight")

            # Get the height of the element
            element_height = element.size["height"]

            print(f"vewport_height: {viewport_height}\n\n")
            print(f"element_height: {element_height}\n\n")

            # Calculate the number of times to scroll to fully reveal the element
            num_scrolls = element_height // viewport_height + 1

            # Execute JavaScript to scroll the element into view incrementally
            for _ in range(num_scrolls * 3):
                time.sleep(0.2)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

        scroll = driver.find_element(By.XPATH, "//div[@class='inner']")
        project_links = listing_element.find_elements(By.XPATH, "//div//ul[@class='listings']//li[@class='property-details property-details-basic']")
        scroll_to_element(driver, scroll)

        time.sleep(5)
        # Find all elements matching the XPath expression
        """
        correct the xpath go more in depth below
        """
        src = "//div[@class='photo']//img[@class='property']"
        srcs = []
        hrefs = []
        link = listing_element.find_elements(By.XPATH, src)

        for i in link:
            z = i.get_attribute("src")
            srcs.append(z)
            print(f"src: {z}\n\n")

        href = "//div[@class='action-bar']//a[@class='btn btn-ghost-primary']"

        links = listing_element.find_elements(By.XPATH, href)
        for i in links:
            z = i.get_attribute("href")
            hrefs.append(z)
            print(f"href: {z}\n\n")
        listing_element.find_elements(By.XPATH, xpath)
        print(f"Found {len(project_links)} project links")
        print(f"Found {project_links} project links")


        for i in project_links:
            listings.append(i.text)
            print(f"i: {i.text}")

        # print(f"listings: {listings}\n\n")
        result = parse_list(listings)
        # for i in result:
        #     i["url"] = links[result.index(i)].get_attribute("href")
        #     i["image"] = link[result.index(i)].get_attribute("src")
        print(f"result: {len(result)}\n\n")
        print(f"hrefs : {len(hrefs)}\n\n")
        print(f"srcs : {len(srcs)}\n\n")
        # for i in result:
        #     print(f"i: {i}\n\n")

        result = update_result(result, hrefs, srcs)

        print(f"result: {result}\n\n")


        driver.quit()

        # except Exception as e:
        #     print(e)
        #     driver.quit()
        #     return None

        return result


def parse_list(list_data):
    parsed_data = []
    for item in list_data:
        item_data = item.strip("'").split("\n")
        if len(item_data) >= 7:
            parsed_item = {
                "Title": item_data[0],
                "address": item_data[1],
                "type": item_data[2],
                "Space": item_data[6]
            }
            parsed_data.append(parsed_item)
    return parsed_data

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


def update_result(result, hrefs, srcs):
  for i in range(len(srcs)):
    result[i].update(href=hrefs[i], src=srcs[i])
  return result
