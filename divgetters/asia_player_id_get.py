import requests
from bs4 import BeautifulSoup
import re

class AsiaFortress():
    def get_div(self, link):
        doc = requests.get(link).text
        soup = BeautifulSoup(doc, 'lxml')
        
        team = None
        lists = soup.find_all(class_='list-group-item')
        for l in lists:
            if 'asiafortress cup' in l.text.lower():
                for x in l.find_all('a', href=True):
                    if 'team' in x['href']:
                        team = x['href']
        
        team_link = 'https://match.tf' + team if team != None else None
        if team_link != None:
            doc = requests.get(team_link).text
            soup = BeautifulSoup(doc, 'lxml')
            lists = soup.find_all('div', class_='panel-heading')
            posdiv = [x.text.strip() for x in lists if 'AsiaFortress' in x.text.strip()][0]
            return 'AsiaFortress - ' + re.findall(r' in (.*?) for ',posdiv)[0]
        else:
            return 'Division 4'