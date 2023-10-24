from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
# Add any additional options if needed
# options.add_argument("--headless")

try:
    # Automatically download and install ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to Google Scholar
    driver.get("https://scholar.google.com/")

    # Wait for a few seconds to let the page load completely
    time.sleep(3)

    # Find the search input field using its name attribute and send keys
    search_input = driver.find_element("name", "q")
    search_input.send_keys("Machine Learning")

    # Simulate pressing the Enter key
    search_input.send_keys(Keys.RETURN)

    # Wait until the 'qs_rs' div element is present on the page
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "qs_rs")))


    # Find the div element with class "qs_rs" and print its text
    div_element = driver.find_element_by_class_name("qs_rs")
    print("Text of div element with class 'qs_rs':", div_element.text)

    # Perform further actions with the driver...

finally:
    # Close the browser window if the driver is defined
    if driver:
        driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# import time

# options = webdriver.ChromeOptions()
# # Add any additional options if needed
# # options.add_argument("--headless")

# try:
#     # Automatically download and install ChromeDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     # Navigate to Google Scholar
#     driver.get("https://scholar.google.com/")

#     # Wait for a few seconds to let the page load completely
#     time.sleep(3)

#     # Find the search input field using its name attribute and send keys
#     search_input = driver.find_element("name","q")
#     search_input.send_keys("Machine Learning")

#     # Simulate pressing the Enter key
#     search_input.send_keys(Keys.RETURN)

#     # Wait for a few seconds to see the search results
#     time.sleep(5)

#     # Perform actions with the driver...

# finally:
#     # Close the browser window if the driver is defined
#     if driver:
#         driver.quit()


