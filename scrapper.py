import requests
from bs4 import BeautifulSoup as bs
import schedule
import time
import csv

def scrape_floodgate_data():
    url='https://bpbd.jakarta.go.id/waterlevel'
    page= requests.get(url)
    soup=bs(page.text,'html')
    table=soup.find('table')
    #loads the raw table with html tags
    with open('floodgate_data.html', 'w') as file:
        file.write(str(table))
    #The table html code will later be loaded to front end
    headers = []
    rows = []
    for header in table.find_all('tr')[1].find_all('td')[1:]:  # Skip the first cell which is empty
        headers.append(header.get_text(strip=True))

    for row in table.find_all('tr')[2:]:  # Skip the header rows
        cells = row.find_all('td')
        if len(cells) > 1:
            row_data = [cell.get_text(strip=True).replace('\xa0', ' ') for cell in cells[1:]]  # Skip the first cell
            rows.append(row_data)
    #csv is needed to make graphs for the floodgate height
    with open('floodgate_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
schedule.every(1).hours.do(scrape_floodgate_data)
if __name__ == "__main__":
    scrape_floodgate_data()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(1)
