from bs4 import BeautifulSoup
import csv

# Read the HTML file
with open('src/table.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <tr> elements with a data-href attribute
tr_elements = soup.find_all('tr', {'data-href': True})

# Extract and print the data-href values
url_list = []
for tr_element in tr_elements:
    data_href_value = tr_element['data-href']
    url_list.append(data_href_value)

# To write to csv, we need list of list

url_master_list = [[url] for url in url_list]

# Specify the CSV file path
csv_file_path = 'data/url_list.csv'

# Write the list to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(url_master_list)

