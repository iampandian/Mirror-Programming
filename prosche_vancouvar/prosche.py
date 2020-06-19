import requests
from bs4 import BeautifulSoup
import pandas as pd

def car_dict(a_listing):
    data = {}
    base_url = 'https://www.porschevancouver.ca'
    data["Name"] = a_listing.find("a", {"class":"vehicle-listing-link"}).text.strip()
    data["Link"] = base_url + a_listing.find("a", {"class":"vehicle-listing-link"})['href']
    data["Color"] = a_listing.find("div", {"class":"vehicle-listing-exterior-color"}).text.strip().replace(" /"," ")
    data["Image"] = a_listing.find("img", {"class":"img-responsive"})['src']
    data["Mileage"] = a_listing.find("div", {"class":"vehicle-listing-mileage"}).text.strip()
    data["Transmission"] = a_listing.find("div", {"class": "vehicle-listing-transmission"}).text.strip()
    data["Price"] = a_listing.find("p", {"class":"vehicle-listing-display-price"}).text.strip()
    return data


headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}

master_list = []

for i in range(1,21):
    print("getting page "+str(i))
    params = (
        ('page', str(i)),
    )
    response = requests.get('https://www.porschevancouver.ca/inventory', headers=headers, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    listings = soup.find_all("div",{"class": "vehicle-listing used"})

    for a_listing in listings:
        listings = car_dict(a_listing)
        master_list.append(listings)


df = pd.DataFrame(master_list)

df.to_csv('prosches.csv', index =False)
