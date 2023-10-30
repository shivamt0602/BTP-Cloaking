import csv
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    'Referer': "https://www.google.com"
}

# Path to the "Bot_src" directory
bot_src_directory = "Normal_src"

# Create "Bot_src" directory if it doesn't exist
if not os.path.exists(bot_src_directory):
    os.makedirs(bot_src_directory)

try:
    with open('twisted_urls.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            url = row[0]
            parsed_url = urlparse(url)
            domain_name = parsed_url.netloc.split('.')[0]  # Extract domain name without the top-level domain suffix
            output_filename = os.path.join(bot_src_directory, f'{domain_name}_srcs.csv')  # Output CSV filename

            # Create srcs file and write data if srcs are found
            try:
                time.sleep(10)
                response_bot = requests.get(url, headers=headers)
                response_bot.raise_for_status()
                soup_bot = BeautifulSoup(response_bot.content, 'html.parser')
                scripts_bot_links = soup_bot.find_all("script")
                bot_src = []

                if scripts_bot_links:
                    for script in scripts_bot_links:
                        src = script.get('src')
                        if src:
                            bot_src.append(src)

                if bot_src:  # If srcs are found, create the CSV file
                    # Write srcs data to a CSV file
                    with open(output_filename, 'w', newline='') as srcs_file:
                        csv_writer = csv.writer(srcs_file)
                        for src in bot_src:
                            csv_writer.writerow([src])
                    print(f"CSV file '{output_filename}' created for {url}")
                else:
                    print(f"No srcs found for {url}, CSV file not created.")

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
