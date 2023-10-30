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

# Path to the "Bot_links" directory
bot_links_directory = "Bot_links"

# Create "Bot_links" directory if it doesn't exist
if not os.path.exists(bot_links_directory):
    os.makedirs(bot_links_directory)

try:
    with open('twisted_urls.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            url = row[0]
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc.split('.')[0]  # Extract domain name without the top-level domain suffix
            output_filename = os.path.join(bot_links_directory, f'{domain_name}_hrefs.csv')  # Output CSV filename

            # Create hrefs list and write data if hrefs are found
            try:
                time.sleep(10)
                response_bot = requests.get(url, headers=headers)
                response_bot.raise_for_status()
                soup_bot = BeautifulSoup(response_bot.content, 'html.parser')
                bot_links = soup_bot.find_all('a')
                bot_hrefs = [link.get('href') for link in bot_links if link and link.get('href')]

                if bot_hrefs:  # If hrefs are found, create the CSV file
                    # Write hrefs data to a CSV file inside the "Bot_links" directory
                    with open(output_filename, 'w', newline='') as hrefs_file:
                        csv_writer = csv.writer(hrefs_file)
                        for href in bot_hrefs:
                            csv_writer.writerow([href])
                    print(f"CSV file '{output_filename}' created for {url}")
                else:
                    print(f"No hrefs found for {url}, CSV file not created.")

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
