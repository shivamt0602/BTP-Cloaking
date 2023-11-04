import os
import csv

def compare_csv_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8', errors='replace') as file1, open(file2_path, 'r', encoding='utf-8', errors='replace') as file2:
        csv_reader1 = csv.reader(file1)
        csv_reader2 = csv.reader(file2)

        # Compare the entire content of the CSV files
        is_different = any(row1 != row2 for row1, row2 in zip(csv_reader1, csv_reader2))

    return is_different

def create_comparison_results(bot_links_folder, normal_links_folder):
    results = []

    # Get a list of common CSV files in the "Bot_links" and "Normal_links" folders
    common_csv_files = set(os.listdir(bot_links_folder)) & set(os.listdir(normal_links_folder))

    for filename in common_csv_files:
        url = filename.split('_hrefs')[0]

        bot_csv_path = os.path.join(bot_links_folder, filename)
        normal_csv_path = os.path.join(normal_links_folder, filename)

        is_different = compare_csv_files(bot_csv_path, normal_csv_path)

        # Append the values to the results list
        results.append({'url': url, 'links_result': -1 if is_different else 1})

    return results

def write_to_csv(results, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'links_result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    # Path to the folders containing CSV files
    bot_links_folder = 'Bot_links'
    normal_links_folder = 'Normal_links'

    # Output CSV file path
    csv_file_path = 'comparison_results_links.csv'
    
    # Create comparison results
    results = create_comparison_results(bot_links_folder, normal_links_folder)

    # Write results to CSV file
    write_to_csv(results, csv_file_path)

    print("Comparison results have been saved to", csv_file_path)
