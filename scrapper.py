import csv
import requests
from bs4 import BeautifulSoup as bs
import re

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
    
    # Save clean data to CSV for each floodgate
    headers = data[0][1:-1]  # Skip 'Pintu Air' and last empty header
    for row in data[1:]:
        floodgate_name = row[0].strip()
        levels = [re.findall(r'\d+', level)[0] if level else '0' for level in row[1:-1]]  # Extract numbers
        
        filename = f'{floodgate_name.replace(" ", "_")}.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Water Level (cm)'])
            for i, level in enumerate(levels):
                writer.writerow([headers[i], level])

if __name__ == "__main__":
    scrape_floodgate_data()