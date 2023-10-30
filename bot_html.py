import csv
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/94.0.4606.71 Safari/537.36",
    'Referer': "https://www.google.com"
}

# Path to the directory where HTML files will be saved
html_files_directory = "Bot_text"

# Create the directory if it doesn't exist
if not os.path.exists(html_files_directory):
    os.makedirs(html_files_directory)

try:
    with open('twisted_urls.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            url = row[0]
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc.split('.')[0]  # Extract domain name without the top-level domain suffix
            output_filename = os.path.join(html_files_directory, f'{domain_name}_content.html')  # Output HTML filename

            # Fetch and save the entire HTML content of the webpage
            try:
                time.sleep(10)
                response_bot = requests.get(url, headers=headers)
                response_bot.raise_for_status()
                html_content = response_bot.content

                # Write HTML content to a file inside the "HTML_files" directory
                with open(output_filename, 'wb') as html_file:
                    html_file.write(html_content)
                print(f"HTML file '{output_filename}' created for {url}")

            except requests.exceptions.HTTPError as errh:
                # Handle HTTP errors
                print(f"HTTP Error for {url}: {errh}")
                continue

            except Exception as e:
                # Handle other errors
                print(f"Error for {url}: {str(e)}")
                continue

except Exception as e:
    # Handle file-related exceptions
    print(f"Error: {str(e)}")
