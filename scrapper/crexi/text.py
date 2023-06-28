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

# Click the checkbox corresponding to the "Retail" choice
wait = WebDriverWait(driver, 10)
checkbox_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/div/div[3]/svg/path"
checkbox = wait.until(EC.visibility_of_element_located((By.XPATH, checkbox_xpath)))
checkbox.click()

# Get the text of the choice
choice_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/label"
choice = driver.find_element(By.XPATH, choice_xpath).text
print(choice)

# Rest of your code...
