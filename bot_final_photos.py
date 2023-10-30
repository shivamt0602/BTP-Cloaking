from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
from selenium.common.exceptions import WebDriverException
import io
import logging
import csv
import os
from urllib.parse import urlparse

# Specify the user agent and referer
user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/94.0.4606.71 Safari/537.36"
referer = "https://www.google.com"

# Create the Bot_photos folder if it doesn't exist
if not os.path.exists('Bot_photos'):
    os.makedirs('Bot_photos')

def capture_full_page_screenshot(url, screenshotFile, user_agent, referer):
    # Set up Chrome options with the specified user agent and referer
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument(f'referer={referer}')
    chrome_options.add_argument('--headless')

    # Initialize the web driver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        time.sleep(20)  # Wait for 5 seconds to allow the page to load properly

        # Handle WebDriverException (e.g., net::ERR_NAME_NOT_RESOLVED)
        if "ERR_NAME_NOT_RESOLVED" in driver.page_source:
            print(f"Error: {url} could not be resolved. Skipping...")
            return

        # Get the page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        # Set the initial viewport height
        viewport_height = driver.execute_script("return window.innerHeight")

        # Capture and stitch the screenshots
        screenshots = []

        for i in range(0, page_height, viewport_height):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(2)  # Adjust sleep time as needed
            screenshot = driver.get_screenshot_as_png()
            screenshots.append(Image.open(io.BytesIO(screenshot)))

        # Stitch the screenshots vertically
        full_page_screenshot = Image.new("RGB", (screenshots[0].width, page_height))
        y_offset = 0

        for screenshot in screenshots:
            full_page_screenshot.paste(screenshot, (0, y_offset))
            y_offset += screenshot.height

        # Save the full-page screenshot
        full_page_screenshot.save(screenshotFile)

    except WebDriverException as e:
        # Log the WebDriverException
        logging.error(f"WebDriverException while processing URL: {url}. Error: {str(e)}")
    except Exception as e:
        # Log other exceptions
        logging.error(f"Exception while processing URL: {url}. Error: {str(e)}")

    finally:
        driver.quit()

# Read URLs from the CSV file and capture screenshots with the specified user agent and referer
with open('twisted_urls.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        url = row[0]
        # Extract domain name from the URL
        # domain = url.split('//')[1].split('/')[0]
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.split('.')[0]  # Extract domain name without the top-level domain 
        # Construct the output file path with user agent and referer information
        output_file = f'Bot_photos/{domain}_{user_agent.replace("/", "_").replace(" ", "_")}.png'
        # Capture the full-page screenshot with the specified user agent, referer, and save it
        capture_full_page_screenshot(url, output_file, user_agent, referer)
