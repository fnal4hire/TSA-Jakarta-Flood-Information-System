import csv
import requests
from bs4 import BeautifulSoup as bs
import re
import os

def scrape_floodgate_data():
    url = 'https://bpbd.jakarta.go.id/waterlevel'
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    
    table = soup.find('table')
    
    # Save the raw HTML table
    with open('floodgate_data.html', 'w', encoding='utf-8') as f:
        f.write(str(table))
    
    # Extract headers from the second row within the <thead> tag
    headers_row = table.find('thead').find_all('tr')[1]  # Get the second row within the <thead> tag
    headers = [header.text.strip() for header in headers_row.find_all('td')[1:-1]]  # Extract header texts, skipping the first and last cells

    data = []
    dict_list=[]

    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            cell_text = cell.text.strip().replace('\xa0', ' ')
            row_data.append(cell_text)
        data.append(row_data)
    
     # Create the list of dictionaries
    for row in data[1:]:  # Skip the header row
        row_dict = {}
        row_dict["nama"] = row[0].strip().replace('\xa0', ' ')  # First cell is the floodgate name
        data_values = [cell.strip().replace('\xa0', ' ') for cell in row[1:len(headers)+1]]  # Extract data values matching the number of headers
        
        # Ensure the data_values length matches headers length
        if len(data_values) < len(headers):
            data_values.extend([''] * (len(headers) - len(data_values)))  # Pad with empty strings
        elif len(data_values) > len(headers):
            data_values = data_values[:len(headers)]  # Truncate excess values
        
        row_dict["data"] = data_values
        dict_list.append(row_dict)   

    directory='.\csv'
    #directory = os.path.join(os.getcwd(), 'csv')
    #os.makedirs(directory, exist_ok=True)
    print(f"Saving files to directory: {directory}")
    # Save clean data to CSV for each floodgate
    for row in data[1:]:
        floodgate_name = row[0].strip()
        levels = [re.findall(r'\d+', level)[0] if level else '0' for level in row[1:-1]]  # Extract numbers
        
        filename = floodgate_name.replace(' ','_')+'.csv'
        filepath= os.path.join(directory, filename)  # Construct the file path
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Water Level (cm)'])
            for i, level in enumerate(levels):
                if i < len(headers):  # Ensure index is within range of headers
                    writer.writerow([headers[i], level])
                else:
                    print(f"Warning: Header not found for level {level} in {floodgate_name}")
    return dict_list
if __name__ == "__main__":
    scrape_floodgate_data()