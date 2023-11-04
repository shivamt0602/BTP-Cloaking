import csv

# Read the CSV file
with open('html.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    rows = list(csv_reader)

# Remove spaces from the 'url' column header
fieldnames = [field.strip() for field in csv_reader.fieldnames]

# Remove spaces from the 'url' column in each row
for row in rows:
    row['url'] = row['url'].strip()

# Write the modified data back to the CSV file
with open('your_modified_csv_file.csv', mode='w', newline='') as new_csv_file:
    csv_writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(rows)

print("Spaces removed from the 'url' column in the CSV.")
