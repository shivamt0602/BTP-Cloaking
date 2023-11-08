import pandas as pd

# Read the CSV file
data = pd.read_csv('comparison_results_html.csv')

# Strip extra spaces from column names
data.columns = data.columns.str.strip()

# Convert 'html_result' column to strings and then strip extra spaces
data['html_result'] = data['html_result'].astype(str).str.strip()

# Strip extra spaces from the 'url' column
data['url'] = data['url'].str.strip()

# Write the cleaned data to a new CSV file
data.to_csv('stripped_html.csv', index=False)