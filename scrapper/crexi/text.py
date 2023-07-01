import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://www.crexi.com/properties?types%5B%5D=Office")

# Wait for the search box to be clickable
search_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.header-typeahead-search-input"))
)

# Click on the search box using JavaScript
driver.execute_script("arguments[0].click();", search_box)

# Wait for the input field to be present in the DOM
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-bar-input"))
)

# Enter the location (e.g., "CA") using JavaScript
driver.execute_script("arguments[0].value = arguments[1];", search_input, "CA")

# Press Enter using JavaScript
driver.execute_script("arguments[0].dispatchEvent(new Event('keydown', { keyCode: 13 }));", search_input)

print("Waiting for the search results to load...")
time.sleep(60)

# Get the HTML response of the opened page
html_response = driver.page_source

# Print the HTML response
print(html_response)

# Close the browser
driver.quit()
