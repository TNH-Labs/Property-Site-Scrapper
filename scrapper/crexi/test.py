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
time.sleep(2)

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

print("Waiting for the search results to load...")
time.sleep(60)

# Get the HTML response of the opened page
html_response = driver.page_source

# Print the HTML response
print(html_response)

# Close the browser
driver.quit()