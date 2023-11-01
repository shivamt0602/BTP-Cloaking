import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Define the URL and the search strings
base_url = "https://sitereview.bluecoat.com/#"

# Initialize the Chrome web driver in headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the website
    driver.get(base_url)

    with open('html.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        
        # Skip the first row (header) and start from the second row
        for row in rows[1:]:
            search_url = row[0].strip() + ".com"  # Remove leading/trailing spaces and add ".com" to the URL
            try:
                # Find the search input element and submit the URL
                search_input = driver.find_element(By.ID, "txtUrl")
                search_input.clear()  # Clear any previous input
                search_input.send_keys(search_url)
                search_input.send_keys(Keys.RETURN)

                # Wait for the results to load
                time.sleep(5)  # You may need to adjust the waiting time

                try:
                    # Find the span element with the class "clickable-category"
                    category_element = driver.find_element(By.CSS_SELECTOR, "span.clickable-category")

                    # Check the text of the span element
                    if category_element.text == "Suspicious":
                        verification = -1
                        print(f"URL: {search_url} - Danger: This URL is categorized as Suspicious")
                    else:
                        verification = 1
                        print(f"URL: {search_url} - No Danger: This URL is not categorized as Suspicious")
                except NoSuchElementException:
                    try:
                        # Find the h2 element with the "Unresolvable Host" text
                        unresolvable_host_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'Unresolvable Host')]")
                        if unresolvable_host_element:
                            verification = 0
                            print(f"URL: {search_url} - Wrong: Unresolvable Host")
                    except NoSuchElementException:
                        verification = -1
                        print(f"URL: {search_url} - Element not found")
                # Append the verification result to the row
                row.append(verification)
            except Exception as e:
                print(f"URL: {search_url} - An error occurred: {e}")

            finally:
                driver.get(base_url)  # Return to the main page

    # Save the updated CSV with the verification column
    with open('comparison_results_html.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

finally:
    # Close the browser
    driver.quit()
