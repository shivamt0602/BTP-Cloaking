import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

# Initialize Chrome web driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the CSV file and create a new CSV file for writing
    with open('comparison_results_html.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Create a list to store updated rows with verification results
        updated_rows = []

        for row in csv_reader:
            url = row['url'] + ".com"  # Add .com to the URL
            expected_result = int(row['html_result'])

            # Open the website
            driver.get("https://sitereview.bluecoat.com/#/")  # Open the base URL

            # Find the search input element and send the URL
            search_input = driver.find_element(By.ID, "txtUrl")
            search_input.clear()
            search_input.send_keys(url)
            search_input.submit()

            # Wait for the page to load (you might need to adjust the waiting time)
            time.sleep(5)  # Adjust the waiting time as needed

            try:
                # Find the specified text in the page source
                page_source = driver.page_source
                if 'This URL is categorized as a security risk' in page_source:
                    actual_result = -1
                else:
                    actual_result = 1

                # Update the 'verification' column in the row dictionary
                row['verification'] = actual_result
                updated_rows.append(row)
            except Exception as e:
                # Handle exceptions, if any
                print(f"URL: {url} - An error occurred: {e}")

    # Write the updated rows with verification results to the original CSV file
    with open('html_results.csv', mode='w', newline='') as updated_csv_file:
        fieldnames = updated_rows[0].keys()
        csv_writer = csv.DictWriter(updated_csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(updated_rows)

finally:
    # Close the browser
    driver.quit()