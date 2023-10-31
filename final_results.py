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

def create_comparison_results(bot_txt_folder, normal_txt_folder):

    results = []
    seen_urls = set()

    # Iterate through files in both folders and compare files with the same names
    for filename in os.listdir(bot_txt_folder):
        value_list = [0] * 4  # Initialize the list with 4 zeros
        bot_file_path = os.path.join(bot_txt_folder, filename)
        normal_file_path = os.path.join(normal_txt_folder, filename)

        url = filename.split('_content')[0]

        # Compare files only if they exist in both folders
        if os.path.isfile(bot_file_path) and os.path.isfile(normal_file_path):
            if url not in seen_urls:
                is_different = compare_html_files(bot_file_path, normal_file_path)
                # Update the list values based on comparison result
                value_list[0] = -1 if is_different else 1  # html_result
                # Add the URL to seen_urls set
                seen_urls.add(url)

                # Append the values to the results list
                results.append({'url': url, 'html_result': value_list[0], 
                                'src_result': value_list[1], 'link_result': value_list[2], 'photos_result': value_list[3]})  

      #write the below code in the same way but check for two folders named Bot_src and Normal_src in these fiind out the same two csvs and compare if these two csvs are  same or not if not same then add -1 to the first index of the value_list                       

    

    return results

def write_to_csv(results, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'html_result', 'src_result', 'link_result', 'photos_result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    # Path to the folders containing HTML files
    bot_txt_folder = 'Bot_text'
    normal_txt_folder = 'Normal_text'
    # Output CSV file path
    csv_file_path = 'comparison_results.csv'
    
    # Create comparison results
    results = create_comparison_results(bot_txt_folder, normal_txt_folder)

    # Write results to CSV file
    write_to_csv(results, csv_file_path)

    print("Comparison results have been saved to", csv_file_path)
