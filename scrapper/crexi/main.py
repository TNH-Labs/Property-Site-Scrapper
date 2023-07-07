import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui as pg
import json
# import pyperclip as pc
# from utils import handle_exception


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from .create_html_posts2 import save_html_post, get_post_element_from_pages



def scrape_crexi(location, category, search_type):
    # service_ = Service(executable_path=r'/scrapper/driver')
    # option = Options()
    # option.add_argument("--headless")
    # option.add_argument("--disable-infobars")
    # # option.add_argument("start-maximized")
    # option.add_argument("--disable-extensions")
    # option.add_argument("--disable-notifications")
    # option.add_argument('--ignore-certificate-errors')
    # option.add_argument('--ignore-ssl-errors')
    # option.add_experimental_option('excludeSwitches', ['enable-   logging'])

    option = Options()
    option.add_argument("--window-size=1920,1080")
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
    try:
        # print(f"Scraping {search_type} {category} in {location}...")
        url = ""
        if search_type == "forSale":
            url = f"https://www.crexi.com/properties?types%5B%5D={category}"
        elif search_type == "forLease":
            url = f"https://www.crexi.com/lease/properties?types%5B%5D={category}"
        elif search_type == "auction":
            url = f"https://www.crexi.com/properties?tradingStatuses%5B%5D=Auction&types%5B%5D={category}"



        # print("url: ",url)
        driver.get(url)
        window_width = driver.execute_script("return window.innerWidth;")
        window_height = driver.execute_script("return window.innerHeight;")

        # Print the width and height
        # print("Window Width:", window_width)
        # print("Window Height:", window_height)

        try:
            pop_up = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "mat-dialog-container"))
            )

            # Close the pop-up by clicking on the close button
            close_button = pop_up.find_element(By.CSS_SELECTOR, "button.cui-modal-close")
            close_button.click()

        except Exception as e:
            print(e)
            # If the pop-up does not appear, continue with scraping the main content
            pass

        # Wait for the search box to be clickable
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-header/crx-header-content/div/div[1]/crx-header-typeahead-search/crx-mobile-search/div/div[4]/div/div/crx-search-bar-pills/form/div"))
        )

        search_box.click()

        # Click on the search box using JavaScript
        driver.execute_script("arguments[0].click();", search_box)

        driver.find_element(By.XPATH,
                            "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-header/crx-header-content/div/div[1]/crx-header-typeahead-search/crx-mobile-search/div/div[4]/div/div/crx-search-bar-pills/form/div/div/input").send_keys(
            f"{location}")
        time.sleep(2)

        pg.press('enter')
        time.sleep(7)

        # Replace the XPath with the correct one for your element
        element_xpath = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results/div/div"

        try:
            pop_up = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "mat-dialog-container"))
            )

            # Close the pop-up by clicking on the close button
            close_button = pop_up.find_element(By.CSS_SELECTOR, "button.cui-modal-close")
            close_button.click()

        except Exception as e:
            print(e)
            # If the pop-up does not appear, continue with scraping the main content
            pass

        time.sleep(20)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, "mat-mdc-slide-toggle-1-button")))
            element.click()
        except:
            b = driver.find_element(By.ID, "mat-mdc-slide-toggle-1-button")
            driver.execute_script("arguments[0].click();", b)

        path = "//a[@class='cover-link'][position()=1]"

        main = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results/div/div/crx-property-tile-aggregate"
        all = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results"
        # listing_element = driver.find_element(By.XPATH, all )
        wait = WebDriverWait(driver, 15)
        listing_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='cover-link'][position()=1]")))
        # print(f"Found {listing_element} listing element")

        pathh = "//a[@class='cover-link']"

        # Find all elements matching the XPath expression
        project_links = listing_element.find_elements(By.XPATH, pathh)


        def scroll_to_element(driver, element):
            # driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
            viewport_height = driver.execute_script("return window.innerHeight")

            # Get the height of the element
            element_height = element.size["height"]

            # Calculate the number of times to scroll to fully reveal the element
            num_scrolls = element_height // viewport_height + 1

            # Execute JavaScript to scroll the element into view incrementally
            for _ in range(num_scrolls):
                time.sleep(0.2)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)

        # Main XPath for the element containing the items
        main_xpath = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div"
        p = "//div[@class='properties-holder properties-holder-map ng-star-inserted']"
        pp = "//div[@class='cls-guard']"
        # Find the main element

        main_element = driver.find_element(By.XPATH, pp)

        # print(f"\n\n main element: {main_element}")

        # Scroll within the main element to load all items
        scroll_to_element(driver, main_element)

        # Find all item elements
        time.sleep(5)
        item_elements = main_element.find_elements(By.XPATH, ".//crx-search-results/div/div/crx-property-tile-aggregate")

        # print(f"\n\n item elements: {item_elements}")
        for item_element in item_elements:
            # Relative XPath for the div element containing the background image URL
            try:
                image_xpath = ".//gallery-item[@class='ng-star-inserted']//gallery-image//div[contains(@class, 'g-image-item')]"
                div_element = item_element.find_element(By.XPATH, image_xpath)
                # print(f"\n\n div element: {div_element}")
                style_attribute = div_element.get_attribute('style')
                image_url = re.search(r"url\(\"(.*?)\"\)", style_attribute).group(1)
                # print(f"Image URL: {image_url}")
            except Exception as e:
                pass

        """
        for index, link in enumerate(project_links, start=1):
            project_url = link.get_attribute('href')
            print(f"Found project URL {index}: {project_url}")
    
        """

        html_response = driver.page_source
        print(f"HTML response: {html_response}....")
        """
        another = driver.find_elements(By.XPATH, "//crx-property-tile-aggregate[@class='ng-star-inserted']")
        print(f"another: {another.text}")
        for i in another:
            print(f"another: {i.text}")
        
        """


        soup = BeautifulSoup(html_response, 'html.parser')

        # Find the container element that holds the listings
        listings_container = soup.find('crx-search-results')
        # print(f"Found {listings_container} listings container")

        # Find all the listing elements within the container
        listings = listings_container.find_all('crx-property-tile-aggregate')
        # print(f"Found {listings} listings")
        # print(listings)
        # Loop through the listings and extract the desired information
        item_data = []  # List to store the item details

        for index, link in enumerate(project_links, start=1):
            project_url = link.get_attribute('href')
            print(f"Found project URL {index}: {project_url}")

            listing = listings[index - 1]  # Get the corresponding listing element

            # Extract the details from each listing element
            try:
                image_url = listing.find('img', {'class': 'ng-lazyloaded'})['src']
            except:
                image_url = None

            if image_url is not None:
                price = listing.find('span', {'class': 'price'}).text.strip()
                title = listing.find('h5', {'class': 'property-name'}).text.strip()
                description = listing.find('div', {'class': 'property-details'}).text.strip()
                address = listing.find('h4', {'class': 'property-address'}).text.strip()
                view_om_button = listing.find('span', text='View OM')

                # Create a dictionary to store the item details
                item = {
                    'image_url': image_url,
                    'price': price,
                    'title': title,
                    'description': description,
                    'address': address,
                    'view_om_button': view_om_button is not None,
                    'url': project_url
                }

                item_data.append(item)

        # Print the item details
        """
        for item in item_data:
            print('Image URL:', item['image_url'])
            print('Price:', item['price'])
            print('Title:', item['title'])
            print('Description:', item['description'])
            print('Address:', item['address'])
            if item['view_om_button']:
                print('View OM Button: Available')
            else:
                print('View OM Button: Not Available')
            print('---')
            
        """

        # Close the browser
        driver.quit()

        return item_data
    except Exception as e:
        print(e)
        driver.quit()
        return None


def replace_spaces_and_commas(string):
    # Replace spaces with dashes
    string = string.replace(" ", "-")
    # Replace commas with dashes
    string = string.replace(",", "-")
    return string
