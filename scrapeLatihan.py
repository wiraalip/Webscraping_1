from bs4 import BeautifulSoup
import requests
import csv

def scrape_hockey(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_hockey_data(soup):
    hockeys = []

    for hockey in soup.find_all('tr'):
        team_name_element = hockey.find('td', class_='name')
        year_element = hockey.find('td', class_='year')
        wins_element = hockey.find('td', class_='wins')
        losses_element = hockey.find('td', class_='losses')
        win_pct_element = hockey.find('td', class_ = 'pct')
        gf_element = hockey.find('td', class_ = 'gf')
        ga_element = hockey.find('td', class_ ='ga')
        
        if team_name_element and year_element:
            team_name = team_name_element.text.strip()
            year = year_element.text.strip()
            wins = wins_element.text.strip()
            losses = losses_element.text.strip()
            win_pct = win_pct_element.text.strip()
            gf = gf_element.text.strip()
            ga = ga_element.text.strip()

            hockeys.append({'Team Name': team_name, 'Year': year, 'Wins': wins, 'Loses': losses, 'Win %': win_pct, 'Goals For (GF)': gf, 'Goals Against (GA)': ga})

    return hockeys


def export_to_csv(data, file_name):
    # Assuming data is a list of dictionaries where each dictionary represents a row in the CSV
    # The keys of the dictionaries will be the CSV headers
    if not data:
        print("Data is empty. Nothing to export.")
        return

    # Extract the headers from the first dictionary in the data list
    headers = data[0].keys()

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write each row (dictionary) to the CSV file
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    url = 'https://www.scrapethissite.com/pages/forms/'
    soup = scrape_hockey(url)

    if soup:
        hockey_data = extract_hockey_data(soup)
        print(hockey_data)

        # Export the data to a CSV file named "hockey_data.csv"
        export_to_csv(hockey_data, "hockey_data.csv")
    else:
        print("Webpage scraping failed.")
