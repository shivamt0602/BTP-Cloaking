import os
import difflib
import csv

def compare_csv_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        file1_content = file1.readlines()
        file2_content = file2.readlines()

    # Compare content of CSV files
    return file1_content == file2_content

# Path to the folders containing HTML and CSV files
bot_src_folder = 'Bot_src'
normal_src_folder = 'Normal_src'

# Output CSV file path
csv_file_path = 'comparison_result.csv'

# Create a dictionary to store URL and corresponding CSV file paths
url_to_csv = {}

# Extract common part of CSV filenames and store in the dictionary
for filename in os.listdir(bot_src_folder):
    if filename.endswith('_srcs.csv'):
        url = filename.split('_srcs')[0]
        bot_csv_path = os.path.join(bot_src_folder, filename)
        normal_csv_path = os.path.join(normal_src_folder, filename)
        url_to_csv[url] = (bot_csv_path, normal_csv_path)

# Read existing CSV data to avoid overwriting existing entries
existing_data = []
if os.path.exists(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        existing_data = list(reader)

# Create a list to store comparison results
results = []

# Iterate through URLs and compare corresponding CSV files
for url, (bot_csv_path, normal_csv_path) in url_to_csv.items():
    # Check if URL is already in existing data
    existing_entry = next((item for item in existing_data if item['url'] == url), None)
    if existing_entry:
        html_result = int(existing_entry['html_result'])
        src_result = int(existing_entry['src_result'])
    else:
        html_result = 0
        src_result = 0

    # Compare CSV files
    csv_diff = compare_csv_files(bot_csv_path, normal_csv_path)

    # Update src_result based on CSV comparison
    if csv_diff:
        src_result = -1
    else:
        src_result = 1

    # Add or update entry in results
    result_entry = {'url': url, 'html_result': html_result, 'src_result': src_result}
    results.append(result_entry)

# Write results to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url', 'html_result', 'src_result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Comparison results have been saved to", csv_file_path)
