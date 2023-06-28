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

# print([type_options.text], "type_options.text")
text = type_options.text
list_items = [item for item in text.split("\n") if item.isalnum()]
print(list_items, "list_items") # returns data like ['All', 'Retail', 'Multifamily', 'Office', 'Industrial', 'Hospitality', 'Land']


wait = WebDriverWait(driver, 10)
# dropdown_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//crx-dropdown-portal//crx-option")))
property_type = "Retail"

checkbox_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/div/div[3]/svg/path"
choice_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/label"
checkbox = driver.find_element(By.XPATH, checkbox_xpath)
checkbox.click()

choice_name = driver.find_element(By.XPATH, choice_xpath).text
print(choice_name)

for i in list_items:
    if i == property_type:
        checkbox_xpath = f"//crx-sales-property-type-filter/crx-multilevel-checkboxes/div[text()='{i}']/../cui-checkbox/mat-checkbox/div"
        checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        checkbox.click()

# wait
time.sleep(5)


# Locate the container element that contains the dropdown options
type_options_container = driver.find_element(By.XPATH, "//crx-sales-property-type-filter/crx-multilevel-checkboxes")

print(type_options_container.text, "type_options_container")
checkbox_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/div"

checkbox = driver.find_element(By.XPATH, checkbox_xpath)

print(checkbox, "checkbox")
checkbox.click()

choice_name_xpath = "/html/body/crx-app/div/crx-home-page/crx-normal-page/div/crx-drawer/mat-drawer-container/mat-drawer-content/div/div/crx-home-hero/div/div[2]/crx-search-tabs/crx-mobile-search/div/div[4]/div[2]/crx-sales-search-form/div/crx-sales-property-type-dropdown/crx-dropdown-form/crx-dropdown-button/div/crx-dropdown-portal/div/div/div[2]/crx-sales-property-type-filter/crx-multilevel-checkboxes/div[2]/cui-checkbox/mat-checkbox/div/label"

choice_name = driver.find_element(By.XPATH, choice_name_xpath).text
print(choice_name)



# Find the specific option by its name
property_type_checkbox = type_options_container.find_element(By.XPATH, f".//div[text()='{property_type}']/../cui-checkbox/mat-checkbox/div")
property_type_label = type_options_container.find_element(By.XPATH, f".//div[text()='{property_type}']/../cui-checkbox/mat-checkbox/div/label")

# Scroll the option into view
driver.execute_script("arguments[0].scrollIntoView(true);", property_type_checkbox)

# Click the checkbox to select the option
property_type_checkbox.click()

# Output the label (optional)
print(property_type_label.text)


# Submit the search
search_button = driver.find_element(By.CSS_SELECTOR, "crx-sales-search-form button.submit-button")
search_button.click()

# Wait for the search results to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "search-results")))

# Get the search results
search_results = driver.find_elements(By.CSS_SELECTOR, "search-result")

# Process the search results as needed
for result in search_results:
    print("Processing search result...")
    print(result.text)
    # Extract relevant information from each search result
    # and perform desired actions

# Close the browser
driver.quit()
