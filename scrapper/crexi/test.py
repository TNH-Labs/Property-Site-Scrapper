from bs4 import BeautifulSoup
from selenium import webdriver
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

service_ = Service(executable_path=r'Properapper/driver')
option = Options()
# option.add_argument("--headless")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_argument("--disable-notifications")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
# option.add_experimental_option('excludeSwitches', ['enable-logging'])

driver  = webdriver.Chrome(options=option, service=service_)
driver.get("https://www.crexi.com/properties?types%5B%5D=Office")


# Wait for the search box to be clickable
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-header/crx-header-content/div/div[1]/crx-header-typeahead-search/crx-mobile-search/div/div[4]/div/div/crx-search-bar-pills/form/div"))
)

search_box.click()

# Click on the search box using JavaScript
driver.execute_script("arguments[0].click();", search_box)

driver.find_element(By.XPATH, "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-header/crx-header-content/div/div[1]/crx-header-typeahead-search/crx-mobile-search/div/div[4]/div/div/crx-search-bar-pills/form/div/div/input").send_keys("CA")
time.sleep(2)

pg.press('enter')
time.sleep(7)

# Replace the XPath with the correct one for your element
element_xpath = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results/div/div"


# element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
# Perform actions on the element once it becomes clickable
# element.click()

# Wait for the pop-up to appear (if it does)
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

# Wait for the input field to be present in the DOM
# search_input = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-header/crx-header-content/div/div[1]/crx-header-typeahead-search/crx-mobile-search/div/div[4]/div/div/crx-search-bar-pills/form/div/div/input"))
# )
#
# search_input.send_keys("CA")

# Enter the location (e.g., "CA") using JavaScript
# driver.execute_script("arguments[0].value = arguments[1];", search_input, "california")
#
# # Press Enter using JavaScript
# driver.execute_script("arguments[0].dispatchEvent(new Event('keydown', { keyCode: 13 }));", search_input)

# print("Waiting for the search results to load...")
time.sleep(15)

path = "//a[@class='cover-link'][position()=1]"

main = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results/div/div/crx-property-tile-aggregate"
all = "/html/body/crx-app/div/ng-component/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/article/div/div/crx-search-grid-view/div/crx-search-grid/div/div/div[1]/crx-search-results"
# listing_element = driver.find_element(By.XPATH, all )
wait = WebDriverWait(driver, 10)
listing_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='cover-link'][position()=1]")))
print(f"Found {listing_element.text} listing element")



# project_link = listing_element.find_element(By.XPATH, path)
# print(f"Found {project_link.text} project link")
#
#
# project_url = project_link.get_attribute('href')
# print(f"Found {project_url} project URL")

pathh = "//a[@class='cover-link']"

# Find all elements matching the XPath expression
project_links = listing_element.find_elements(By.XPATH, pathh)

# Loop through the elements and retrieve their URLs
for index, link in enumerate(project_links, start=1):
    print(f"Found project link {index}: {link.text}")
    project_url = link.get_attribute('href')
    print(f"Found project URL {index}: {project_url}")


# image path:
image_element = "//gallery-item[@class='g-active-item ng-star-inserted']"
-----------------

# element_ = "//crx-property-tile-aggregate[@class='ng-star-inserted'][position()=1]"
# listing_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='cover-link'][position()=1]")))
#
# # Find all elements matching the XPath expression
# project_links = listing_element.find_elements(By.XPATH, element_)
#
# # Loop through the elements and retrieve their URLs
# for index, link in enumerate(project_links, start=1):
#     print(f"Found project link {index}: {link.text}")
#     project_url = link.get_attribute('href')
#     print(f"Found project URL {index}: {project_url}")

# Get the HTML response of the opened page
html_response = driver.page_source

# print(html_response,"....")

# Print the HTML response
# print(html_response)
# Parse the HTML response using BeautifulSoup
soup = BeautifulSoup(html_response, 'html.parser')

# Find the container element that holds the listings
listings_container = soup.find('crx-search-results')
# print(f"Found {listings_container} listings container")

# Find all the listing elements within the container
listings = listings_container.find_all('crx-property-tile-aggregate')
# print(f"Found {listings} listings")
# print(listings)
# Loop through the listings and extract the desired information
for listing in listings:
    # print(f"Found {listing} listing")
    # Extract the details from each listing element
    try:
        image_url = listing.find('img', {'class': 'ng-lazyloaded'})['src']
    except:
        image_url = None
    price = listing.find('span', {'class': 'price'}).text.strip()
    title = listing.find('h5', {'class': 'property-name'}).text.strip()
    description = listing.find('div', {'class': 'property-details'}).text.strip()
    address = listing.find('h4', {'class': 'property-address'}).text.strip()
    view_om_button = listing.find('span', text='View OM')
    # link_element = listing.find_element(By.TAG_NAME, 'a')

    # Print the extracted details
    print('Image URL:', image_url)
    print('Price:', price)
    print('Title:', title)
    print('Description:', description)
    print('Address:', address)
    if view_om_button:
        print('View OM Button: Available')
    else:
        print('View OM Button: Not Available')
    print('---')


# Close the browser
driver.quit()