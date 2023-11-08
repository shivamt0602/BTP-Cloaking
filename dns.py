import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Define user agents
# user_agents = {
#     "googleua": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
#     "googlebotua": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# }

# Common options for the Chrome driver
common_options = webdriver.ChromeOptions()
# common_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Initialize the Chrome driver outside of the loop
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=common_options)

co = 1

try:
    # Read URLs from the CSV file and iterate over them
    with open('tranco.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:

            if(co>5):
                break
            tranco_number, original_domain = row[0], row[1]

            # Navigate to DNSTwister report page
            driver.get("https://dnstwister.report/")

            # Wait for a few seconds to let the page load completely
            time.sleep(3)

            # Find the search input field using its name attribute and send keys
            search_input = driver.find_element("name", "domains")
            search_input.clear()  # Clear any previous input
            search_input.send_keys(original_domain)

            # Simulate pressing the Enter key
            search_input.send_keys(Keys.RETURN)

            # Wait until the 'qs_rs' div element is present on the page
            time.sleep(90)

            # Find and format URLs
            td_elements = driver.find_elements("xpath", "//table[@id='main_report']//tbody//tr//td[1]")
            domain_list = [td_element.text for td_element in td_elements]
            formatted_urls = ['https://' + url if not url.startswith(('http://', 'https://')) else url for url in domain_list]

            # Write formatted URLs to a CSV file named after the original domain
            with open(f'{original_domain}_twisted.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Twisted URLs'])  # Write header
                csv_writer.writerows([[url] for url in formatted_urls])  # Write each URL on a new line
            co += 1    

finally:
    # Close the browser window
    driver.quit()