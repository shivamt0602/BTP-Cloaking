from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the driver outside the try block
driver = None

options = webdriver.ChromeOptions()
# Add any additional options if needed
# options.add_argument("--headless")  # Run Chrome in headless mode

# try:
#     # Automatically download and install ChromeDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     # Navigate to Google Scholar
#     driver.get("https://www.techwithtim.net/tutorials")

#     # Wait for a few seconds to let the page load completely
#     time.sleep(5)

#     # Wait until the element with the link text "Get started" is clickable
#     link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Get started")))
#     link.click()

#     driver.back()

#     time.sleep(5)

#     # Continue with your automation...

# finally:
#     # Close the browser window if the driver is defined
#     if driver:
#         driver.quit()


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.techwithtim.net/tutorials")

# Wait until the element with the link text "Get started" is clickable
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Get started")))
link.click()