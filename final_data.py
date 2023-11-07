import csv

file_paths = ["stripped_html", "stripped_links", "stripped_photos", "stripped_src"]

urlDict = {}
valDict = {}

for i, file in enumerate(file_paths):
    # Specify the file path
    file_path = f'{file}.csv'

    # Open the CSV file in read mode and specify the delimiter if it's different from a comma
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)
    
        # Skip the header row
        next(csv_reader)
        
        # Iterate through the rows and print the data
        for row in csv_reader:
            # print(row)
            if row[0] not in urlDict:
                urlDict[row[0]] = [0, 0, 0, 0]
            if row[0] not in valDict:
                valDict[row[0]] = int(row[2])
            urlDict[row[0]][i] = int(row[1])

csv_arr = [
    ["url", "html_result", "links_result", "ocr_result", "src_result", "Value"]
]
acc_arr = []

for key in urlDict:
    row = urlDict[key]
    thisRow = [
        key, row[0], row[1], row[2], row[3], valDict[key]
    ]
    csv_arr.append(thisRow)
    acc_arr.append(int(valDict[key] in row))

# Specify the file path
file_path = 'final_output.csv'

# Open the CSV file in write mode with the specified encoding
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csv_writer = csv.writer(csvfile)
    
    # Write the data to the CSV file
    csv_writer.writerows(csv_arr)

print(f'CSV file "{file_path}" has been created.')

# Specify the file path and name
file_path = 'output.txt'

# Open the file in write mode ('w')
# If the file doesn't exist, it will be created; if it exists, its contents will be overwritten
with open(file_path, 'w') as file:
    # Write content to the file
    file.write(f'Accuracy: {100*sum(acc_arr)/len(acc_arr)}%')

print(f'File "{file_path}" has been created.')