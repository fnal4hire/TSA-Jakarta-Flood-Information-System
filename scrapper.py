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
    
    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            cell_text = cell.text.strip().replace('\xa0', ' ')
            row_data.append(cell_text)
        data.append(row_data)
    
    # Extract headers from the second row within the <thead> tag
    headers_row = table.find('thead').find_all('tr')[1]  # Get the second row within the <thead> tag
    headers = [header.text.strip() for header in headers_row.find_all('td')[1:-1]]  # Extract header texts, skipping the first and last cells
    directory='.\csv'
    #directory = os.path.join(os.getcwd(), 'csv')
    #os.makedirs(directory, exist_ok=True)
    print(f"Saving files to directory: {directory}")
    # Save clean data to CSV for each floodgate
    for row in data[1:]:
        floodgate_name = row[0].strip()
        levels = [re.findall(r'\d+', level)[0] if level else '0' for level in row[1:-1]]  # Extract numbers
        
        filename = f'{floodgate_name.replace(" ", "_")}.csv'
        filepath= os.path.join(directory, filename)  # Construct the file path
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Water Level (cm)'])
            for i, level in enumerate(levels):
                if i < len(headers):  # Ensure index is within range of headers
                    writer.writerow([headers[i], level])
                else:
                    print(f"Warning: Header not found for level {level} in {floodgate_name}")

if __name__ == "__main__":
    scrape_floodgate_data()