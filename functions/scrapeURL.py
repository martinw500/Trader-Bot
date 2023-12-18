import requests
from bs4 import BeautifulSoup

def webScraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            print(link.get('href'))
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def webScraperTable(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        if tables:
            target_table = tables[0]
            headers = [header.text.strip() for header in target_table.find_all('th')]
            rows = []
            for row in target_table.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                if row_data:
                    rows.append(row_data)
            print(headers)
            for row in rows:
                print(row)
        else:
            print("No tables found on the webpage.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
