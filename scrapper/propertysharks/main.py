import ast
import urllib

import requests
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
import urllib.parse
import urllib.request
from ..CSV import save_dict_to_csv




def scrape_propertysharks(search_type, category, location):
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
    # try:

        driver = webdriver.Chrome("./chromedriver.exe", options=option)
        # Perform scraping based on the selected search type and form data
        print("\n\nScraping propertysharks...")
        print(f"Search type: {search_type}")
        print(f"Property name: {category}")
        print(f"Location: {location}\n\n")
        action = ActionChains(driver)
        category_mappings = {
            'Office': 'office',
            'Industrial': 'industrial',
            'Retail': 'retail',
            'Retail Space': 'retail',
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
            'Restaurants': 'commercial-real-estate',
            'Office Space': 'office',
            'Medical': 'commercial-real-estate',
            'Medical Offices': 'commercial-real-estate',
            'Coworking': 'office',
            'Senior Housing': 'commercial-real-estate',
            'All Spaces': 'commercial-real-estate'
        }

        if search_type == 'forRent' or search_type == 'forLease':
            search_type = 'Lease'
        elif search_type == 'forSale':
            search_type = 'Sale'

        print(f"search_type: {search_type}")
        print(f"cateogry: {category}")

        category_name = category_mappings[category]
        #
        print(f"category_name: {category_name}")


        location = replace_spaces_and_commas(location)

        print(f"category_name: {category_name}")
        print(f"location: {location}")


        # Construct the URL
        url = ""
        if category_name != 'office' or category_name != 'industrial' or category_name != 'retail':
            if search_type == 'Sale':
                url = f"https://www.propertyshark.com/cre/for-sale/{category_name}/us/{location}/?IncludeCoworking=false&CoworkingWorkspaceTypes=0"
            else:
                url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Land':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=4&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name != 'flex-space':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=5&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Agriculture':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=6&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name != 'commercial-real-estate' and category == 'Hotel and Motel':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=7&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Senior and Housing':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=8&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Health Care':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=9&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Sports and Entertainment':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=10&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Special Purpose':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=11&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Mixed Use':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=12&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Multi-Family':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=13&ListingType={search_type}&CoworkingWorkspaceTypes=0"
        elif category_name == 'commercial-real-estate' and category == 'Events':
            url = f"https://www.propertyshark.com/cre/{category_name}/us/{location}/?IncludeCoworking=false&PropertyTypes=16&ListingType={search_type}&CoworkingWorkspaceTypes=0"



        print(f"Scraping {url}...")
        url = replace_spaces_and_commas(url)
        # url = quote_plus(url)

        print(f"Scraping {url}...")


        print("Before response...")
        # Make the request with the selected proxy and parameters
        # client = ZenRowsClient("e810791d06d06c2bba5a8ee7696f03d65385c0cd")
        # params = {"autoparse": "true"}
        client = ZenRowsClient("8cb92d04c60beddcb5a5f13c119f96f566525144")
        # url = "https://www.loopnet.com/"
        params = {"autoparse": "true"}

        response = client.get(url, params=params)

        # print(response.text)
        print("After response...")
        response.raise_for_status()
        # response = client.get(url, params=params)

        # print(f"response: {response}\n\n")
        # print(f"response.text: {response.text}\n\n")

        # print(response.text)
        # print(response.text, "response3")
        print("After response...")
        # response.raise_for_status()

        listings = []

        if search_type == 'auctions':
            print("yes it iis auctions")


        driver.get(url)
        time.sleep(1)

        path = "onetrust-accept-btn-handler"

        cookie_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, path))
        )
        cookie_box.click()


        filter_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdownMore"))
        )
        filter_box.click()


        apply_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/form/div/div[1]/div[2]/div/div/div[3]/button[1]"))
        )
        apply_box.click()

        time.sleep(3)

        xpath = "//div//ul[@class='listings']/li"

        # fin = driver.find_element(By.XPATH, xpath)
        # print(fin.get_attribute('id'), "-------//////////////////")
        # print(fin.text)


        # for i in fin:
        #     # i.get_attribute('id')
        #     # print(i.text,"***************************")
        #     fin_id = driver.find_element(By.XPATH, i)
        #     print(fin_id.get_attribute('id'))
        #     # print(i.get_attribute('id'), "-------//////////////////")

        # try:
        # print("url: ",url)
        # listing_element = driver.find_element(By.XPATH, all )
        wait = WebDriverWait(driver, 20)
        listing_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        # print(f"Found {listing_element} listing element")


        def scroll_to_element(driver, element):
            viewport_height = driver.execute_script("return window.innerHeight")

            # Get the height of the element
            element_height = element.size["height"]

            # print(f"vewport_height: {viewport_height}\n\n")
            # print(f"element_height: {element_height}\n\n")

            # Calculate the number of times to scroll to fully reveal the element
            num_scrolls = element_height // viewport_height + 1

            # Execute JavaScript to scroll the element into view incrementally
            for _ in range(num_scrolls * 3):
                time.sleep(0.2)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)


        scroll = driver.find_element(By.XPATH, "//div[@class='inner']")
        project_links = listing_element.find_elements(By.XPATH, "//div//ul[@class='listings']//li[@class='property-details property-details-basic']")

        time.sleep(5)
        scroll_to_element(driver, scroll)

        # Find all elements matching the XPath expression
        """
        correct the xpath go more in depth below
        """
        fin_container = driver.find_elements(By.XPATH, xpath)
        lis = []
        srcs = []
        hrefs = []
        for i in range(1,len(fin_container)):
            single_container = driver.find_element(By.XPATH, f"//div//ul[@class='listings']/li[{i}]")
            container = driver.find_element(By.XPATH, f"//div//ul[@class='listings']/li[@id={single_container.get_attribute('id')}]")
            listings.append(container.text)
            lis.append(single_container.get_attribute("id"))
            image_url = single_container.find_element(By.XPATH, "//div[@class='item-presentation']/div/img")
            url = single_container.find_element(By.XPATH, "//div[@class='item-information']/div[@class='action-bar']/a")
            srcs.append(image_url.get_attribute("src"))
            hrefs.append(url.get_attribute("href"))
            print(container.text)
            # print(single_container.get_attribute("id"))
            # print(image_url.get_attribute("src"))
            # print(url.get_attribute("href"))

        # print(lis, "liss")
        # src = "//class[@id='map_container']/div[2]/div[3]/div/div[1]"
        # # action.move_to_element(src).perform()
        # time.sleep(3)
        # srcs = []
        # hrefs = []
        # # wait = WebDriverWait(driver, 25)
        # # wait.until(EC.presence_of_element_located((By.XPATH, src)))
        # link = driver.find_elements(By.XPATH, src)
        #
        # for i in link:
        #     z = i.get_attribute("src")
        #     srcs.append(z)
        #     print(f"src: {z}\n\n")
        #
        # href = "//div//ul[@class='listings']//div[@class='action-bar']//a[@class='btn btn-ghost-primary']"
        #
        # links = listing_element.find_elements(By.XPATH, href)
        # for i in links:
        #     z = i.get_attribute("href")
        #     hrefs.append(z)
        #     # print(f"href: {z}\n\n")
        # listing_element.find_elements(By.XPATH, xpath)
        # print(f"Found {len(project_links)} project links")
        # print(f"Found {project_links} project links")


        # for i in project_links:
        #     print(i.text, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #     listings.append(i.text)
            # print(f"i: {i.text}")

        # print(f"listings: {listings}\n\n")
        result = parse_list(listings)
        # print(f"result: {len(result)}\n\n")
        # print(f"hrefs : {len(hrefs)}\n\n")
        # print(f"srcs : {len(srcs)}\n\n")

        result = update_result(result, hrefs, srcs)
        print(f"result sharks: {result}\n\n")

        # print(f"result: {result}\n\n")


        driver.quit()

        # except Exception as e:
        #     print(e)
        #     driver.quit()
        #     return None

        return result

    # except Exception as e:
    #     print(e)
    #     driver.quit()


def parse_list(list_data):
    parsed_data = []
    for item in list_data:
        item_data = item.strip("'").split("\n")
        if len(item_data) >= 7:
            # try:
            #     print(item_data, "//////-------------------")
            #     print(item_data[1].strip(",")[2:], "&&&&&&&&&&&&&&&&&")
            #     print(item_data[1].strip(","), "&&&&&&&&&&&&&&&&&")
            #     print(item_data[1].strip(",").split(","), "&&&&&&&&&&&&&&&&&")
            #     print(item_data[1].strip(",").split(",")[-2], "^^^^^^^^^^^^^^^^^^^^^")
            #     print(item_data[1].strip(",").split(",")[-2:], "^^^^^^^^^^^^^^^^^^^^^")
            #     print(item_data[1].strip(",").split(",")[:-2:], "^^^^^^^^^^^^^^^^^^^^^")
            # except:
            #     pass
            if item_data[3][0] == '$' or item_data[3] == 'Contact for pricing':
                print("access if")

                parsed_item = {
                    "name": item_data[0],
                    "description": item_data[3],
                    "price": item_data[3] if item_data[3][1] == '$' else "Undisclosed",
                    "address": item_data[0],
                    "locality": item_data[1].strip(" ").split(",")[-2],
                    "region": item_data[1].strip(" ").split(",")[-1],
                }
            elif item_data[3][0] != '$' or item_data[3] != 'Contact for pricing':
                # print("access else")
                # print(item_data, "-------------------))()()()())")
                # print(item_data[3][1], ")(()()---------------090909")
                #
                #
                # print(item_data, "//////-------------------")
                # print(item_data[3].strip(",")[2:], "&&&&&&&&&&&&&&&&&")
                # print(item_data[3].strip(","), "&&&&&&&&&&&&&&&&&")
                # print(item_data[3].strip(",").split(","), "&&&&&&&&&&&&&&&&&")
                # print(item_data[3].strip(",").split(",")[-2:], "^^^^^^^^^^^^^^^^^^^^^")
                # print(item_data[3].strip(",").split(",")[:-2:], "^^^^^^^^^^^^^^^^^^^^^")
                # print(item_data[3].strip(",").split(",")[-2], "^^^^^^^^^^^^^^^^^^^^^")
                try:

                    print("--------------------------1st try -------------------------")
                    parsed_item = {
                        "name": item_data[1],
                        "description": item_data[2],
                        "price": "Undisclosed",
                        "address": item_data[3],
                        "locality": item_data[3].strip(" ").split(",")[-2],
                        "region": item_data[1].strip(" ").split(",")[-1],
                    }
                except:
                    print("--------------------------2nd except -------------------------")
                    parsed_item = {
                        "name": item_data[1],
                        "description": item_data[2],
                        "price": "Undisclosed",
                        "address": item_data[3],
                        "locality": item_data[3].strip(" ").split(",")[-2],
                        "region": item_data[1].strip(" ").split(",")[-1],
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
    print(f"words: {words}...")

    # If there are exactly two words
    if len(words) == 2:
        # if there is a comma in the string then remove it
        for i in range(len(words)):
            if "," in words[i]:
                words[i] = words[i].replace(",", "")

        # Reverse the order and join with a slash
        new_string = "/".join(words[::-1])
    elif len(words) > 2:
        # If there are more than two words, last one should go to first with '/' like 'word/' and rest having spaces should replaced with '-' so final string can be 'word/word-word'
        new_string = words[-1] + "/"
        for i in range(len(words) - 1):
            if "," in words[i]:
                words[i] = words[i].replace(",", "")
            new_string += words[i] + "-"
        new_string = new_string[:-1]
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
    try:
      for i in range(len(srcs)):
        result[i].update(href=hrefs[i], src=srcs[i])
    except:
        for i in range(len(result)):
            result[i].update(href=hrefs[i], src=srcs[i])

    return result
