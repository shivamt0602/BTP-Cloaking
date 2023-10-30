import os
import difflib
import csv

def compare_html_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        file1_content = file1.readlines()
        file2_content = file2.readlines()

    # Use difflib to compare the content of the two files
    d = difflib.Differ()
    diff = list(d.compare(file1_content, file2_content))

    # Check if there are differences in the files
    is_different = any(line.startswith('-') or line.startswith('+') for line in diff)

    return is_different

# Path to the folders containing HTML files
bot_txt_folder = 'Bot_text'
normal_txt_folder = 'Normal_text'

# Output CSV file path
csv_file_path = 'comparison_results.csv'

# Create a list to store comparison results
results = []

# Iterate through files in both folders and compare files with the same names
for filename in os.listdir(bot_txt_folder):
    bot_file_path = os.path.join(bot_txt_folder, filename)
    normal_file_path = os.path.join(normal_txt_folder, filename)
    
    # Compare files only if they exist in both folders
    if os.path.isfile(bot_file_path) and os.path.isfile(normal_file_path):
        is_different = compare_html_files(bot_file_path, normal_file_path)
        url = filename.split('_content')[0]  # Extract URL from filename
        result = -1 if is_different else 1
        results.append({'url': url, 'comparison_result': result})

# Write results to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url', 'comparison_result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Comparison results have been saved to", csv_file_path)
