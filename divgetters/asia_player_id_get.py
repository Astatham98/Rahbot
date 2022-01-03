import requests
from bs4 import BeautifulSoup
import re

class AsiaFortress():
    def get_div(self, link):
        doc = requests.get(link).text
        soup = BeautifulSoup(doc, 'lxml')
        
        team = None
        lists = soup.find_all(class_='list-group-item')
        
        i=0
        found = False
        while i <= len(lists)-1 and not found:
            if 'played in asiafortress cup' in lists[i].text.lower():
                for x in lists[i].find_all('a', href=True):
                    if 'team' in x['href']:
                        team = x['href']
                        found=True
            i+=1
        
        team_link = 'https://match.tf' + team if team != None else None
        print(team_link)
        if team_link != None:
            doc = requests.get(team_link).text
            soup = BeautifulSoup(doc, 'lxml')
            lists = soup.find_all('div', class_='panel-heading')
            posdiv = [x.text.strip() for x in lists if 'AsiaFortress Cup' in x.text][0]
            return ['AsiaFortress - ' + re.findall(r' in (.*?) for ',posdiv)[0] + ' ' + "6's"]
        else:
            return ['AsiaFortress - Division 4' + ' ' + "6's"]
        
