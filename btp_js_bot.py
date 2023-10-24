import csv
import requests
from bs4 import BeautifulSoup
import time

# Define user agents
# user_agents = {
#     "googleua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
#     "googlebotua": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
# }

headers = {
    'User-Agent': "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36"
}

try:
    # Open the CSV file containing twisted URLs
    flag = True # start with a flag that records cloaking present not not finally

    with open('amazonaws.com_twisted.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Iterate over the first 10 URLs in the CSV file
        for row in csv_reader:

            url = row[0]

            # Request the URL using different user agents and get the number of hrefs
            try:
                time.sleep(10)
                # --------------Request using Googlebot user agent----------------
                response_googlebot = requests.get(url, headers=headers)
                response_googlebot.raise_for_status()  # Raise HTTPError for bad requests
                soup_googlebot = BeautifulSoup(response_googlebot.content, 'html.parser')
                # bot_links = soup_googlebot.find_all('a')
                scripts_bot_links =  soup_googlebot.find_all("script") 
                bot_src = []

                if soup_googlebot:
                    if scripts_bot_links:
                        for script in scripts_bot_links:
                            src = script.get('src')
                            if src:
                                bot_src.append(src) 
                

                num_src_googlebot = len(bot_src)                    

                # # --------------Request using regular user agent--------------

                # response_normal = requests.get(url)
                # response_normal.raise_for_status()  # Raise HTTPError for bad requests
                # soup_normal = BeautifulSoup(response_normal.content, 'html.parser')
                # normal_links = soup_googlebot.find_all('a')
                # # num_hrefs_normal = len(normal_links)
                # normal_hrefs = []

                # if soup_normal:
                #     if normal_links:
                #         for link in normal_links:
                #             if link:
                #                 href = link.get('href')
                #                 if href:
                #                     normal_hrefs.append(href) 

                # num_hrefs_normal = len(normal_hrefs)                    

                # Record the results in a txt file,this file is just for recording
                with open('src_counts_bot.txt', 'a') as file:
                    file.write(f"URL: {url}\n")
                    file.write(f"Number of HREFs (Googlebot): {num_src_googlebot}\n")
                    # file.write(f"Number of HREFs (Normal): {num_hrefs_normal}\n\n")

                # if(num_hrefs_googlebot!=num_hrefs_normal):
                #     flag = False
                #     with open('links_dissimilarity_counts.txt','a') as f1:
                #         f1.write(f"URL: {url}\n")
                #         f1.write(f"Number of HREFs (Googlebot): {num_hrefs_googlebot}\n")
                #         f1.write(f"Number of HREFs (Normal): {num_hrefs_normal}\n\n")


                # else:
                #     ## will have to check each and every hrefs here according to the bot and normal user agent     
                #     size = len(normal_hrefs) 

                #     for i in range(0,size):
                #         if(normal_hrefs[i]!=bot_hrefs[i]):
                #             flag = False
                #             with open('links_dissimilarity_content.txt','a') as f2:
                #                 f2.write(f"{normal_hrefs[i],bot_hrefs[i]}")

                # Introduce a delay of 1 second between requests

            except requests.exceptions.HTTPError as errh:
                # Handle HTTP errors
                with open('href_src__counts.txt', 'a') as file:
                    file.write(f"URL: {url}\n")
                    file.write(f"HTTP Error: {errh}\n\n")
                continue

            except Exception as e:
                # Handle other exceptions
                with open('href_src__counts.txt', 'a') as file:
                    file.write(f"URL: {url}\n")
                    file.write(f"Error: {str(e)}\n\n")
                continue

except Exception as e:
    # Handle file-related exceptions
    print(f"Error: {str(e)}")
