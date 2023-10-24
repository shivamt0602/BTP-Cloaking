import csv
import requests
from bs4 import BeautifulSoup

# Assuming you have a CSV file named 'input.csv'
csv_file = 'phishy.csv'

list_urls = []  # Initialize the list here

# Open the CSV file and read URLs from the 'URL' column
with open(csv_file, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Iterate through each row and append the URL from the 'URL' column to the list
    for row in csv_reader:
        list_urls.append(row['URL'])

# Counter for total scripts found
co = 1

# User agents for Google and Googlebot
google_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
googlebot_ua = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

for url in list_urls:
    if co > 5:
        break

    print(f"Checking {url}:")

    try:
        # Send a GET request to the URL with Google UA
        response_google_ua = requests.get(url, headers={"User-Agent": google_ua})
        response_google_ua.raise_for_status()  # Raise an HTTPError for bad requests
        
        # Send a GET request to the URL with Googlebot UA
        response_googlebot_ua = requests.get(url, headers={"User-Agent": googlebot_ua})
        response_googlebot_ua.raise_for_status()  # Raise an HTTPError for bad requests

        soup_google_ua = BeautifulSoup(response_google_ua.content, 'html.parser')
        soup_googlebot_ua = BeautifulSoup(response_googlebot_ua.content, 'html.parser')

        # Compare HTML content length
        len_google_ua = len(soup_google_ua.prettify())
        len_googlebot_ua = len(soup_googlebot_ua.prettify())

        with open("cloaking_detection_comparison.txt", "a") as f:
            if len_googlebot_ua != len_google_ua:
                f.write(f" {url} {len_google_ua} {len_googlebot_ua} cloaking detected \n") 

                # Write Google UA content to a file
                with open(f"{co}_ua.txt", "w", encoding="utf-8") as ua_file:
                    ua_file.write(soup_google_ua.prettify())

                # Write Googlebot UA content to a file
                with open(f"{co}_bot.txt", "w", encoding="utf-8") as bot_file:
                    bot_file.write(soup_googlebot_ua.prettify())   

            else:
                f.write(f"{url} {len_google_ua} {len_googlebot_ua} no cloaking \n") 

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Moving on to the next URL.")
        continue
    
    print("-" * 50)  # Separate output for different URLs 
    co += 1

print("Total scripts found:", co)
