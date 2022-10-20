import re

import bs4
import requests
from fake_useragent import UserAgent


url = 'https://www.sut.ru/studentu/raspisanie/raspisanie-sessii-studentov-zaochnoy-formi-obucheniya?group=55287'
user_agent = UserAgent().firefox
headers = {'User-Agent': user_agent}

response = requests.get(url, headers=headers)

# TODO: Check response.status_code == 200

soup = bs4.BeautifulSoup(response.text, 'html.parser')

pairs = soup.find_all("tr", class_="pair")
# TODO: check if pairs is None

date_pattern = r'\d{1,3}\.\d{1,3}\.\d{4}'
time_pattern = r'\d\d\.\d\d-\d\d\.\d\d'
events = []

for pair in pairs:
    row = pair.find_all("td")
    event = {
        "date": re.findall(date_pattern, row[0].text)[0].replace('.', '-'),
        "time": re.findall(time_pattern, row[1].text)[0].replace('.', ':'),
        "format": row[2].text.strip(),
        "subject": row[3].text.strip(),
        "teacher": row[4].text.strip(),
        "classroom": row[5].text.split(";")[0].strip() + "/" + row[5].text.split("к.")[-1].strip()
    }
    if "История" in event["subject"]:
        event["subject"] = "История"
    events.append(event)
