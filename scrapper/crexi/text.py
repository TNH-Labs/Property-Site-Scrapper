import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://www.crexi.com/")

# Wait for the search input field to be visible
search_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "crx-search-bar input.search-bar-input"))
)

# Enter the location in the search input field
location = "CA"
search_input.send_keys(location)

# Select the "Type" dropdown and choose a property type
type_dropdown = driver.find_element(By.CSS_SELECTOR, "crx-sales-property-type-dropdown crx-dropdown-button")
type_dropdown.click()

# Wait for the property type options to be visible
type_options = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes"))
)

# Get the text of the choice
choices_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes"
choices_elements = driver.find_elements(By.XPATH, choices_xpath)
# print(f"Number of choices: {len(choices_elements)}")
# print(f"Choice text[0]: {choices_elements[0].text}")
# print(f"Choice text: {choices_elements}")
# Loop through the choices and click on the desired one
desired_choice_text = "Retail"  # Replace with your desired choice text

if desired_choice_text == "Retail":
    choice_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]"
    choice = driver.find_element(By.XPATH, choice_xpath).text
    print(f"Choice: {choice}")
    check = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/div/input"
    driver.find_element(By.XPATH, check).click()
    time.sleep(5)
    search_button = driver.find_element(By.XPATH, "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/div/crx-search-bar/form/button")
    search_button.click()
    time.sleep(15)

    # Get the HTML response of the opened page
    html_response = driver.page_source

    # Print the HTML response
    print(html_response)
# for choice_element in choices_elements:
#     print(f"Choice text: {choice_element.text}")
#     if choice_element.text == desired_choice_text:
#         print("Found desired choice")
#         choice_element.click()
#         break
# Rest of your code...
