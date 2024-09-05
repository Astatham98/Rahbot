import requests
from collections import Counter
from time import sleep
import time    


class Etf2l():
    def get_div(self, etf2l, sixes=True):
        split = etf2l.split('/')
        id = split[-2]
        gamemodes = ['Highlander', '6v6']

        response  = requests.get('https://api.etf2l.org/player/{}/results.json?per_page=100&since=0'.format(id))
        
        divs = []
        for gamemode in gamemodes:
            if response.status_code == 200:
                json_format = response.json()
                competitions = json_format['results']
                div ='Open'
                try:
                    for c in competitions:
                        comp = c['competition']
                        if comp['type'] == gamemode and c['merced'] == 0 and 'preseason' not in comp['name'].lower():
                            if c['division']['name'] is not None:
                                div = c['division']['name']
                                break
                except TypeError:
                    div = 'Open'
                
                divs_split = [x for x in div]
                div = ''.join(divs_split[:-1]) if divs_split[-1] in ('A', 'B') else ''.join(divs_split)

                div = "".join(div.split(" ")[:-1]) if div.split(" ")[-1] == 'Division' else div

                
                ender = gamemode if gamemode != '6v6' else "6's"
                divs.append('Etf2l - ' + div + ' ' + ender)
        print(divs)
        return divs
    
    def get_steam(etf2l):
        split = etf2l.split('/')
        id = split[-2]
        response  = requests.get('https://api.etf2l.org/player/{}.json?per_page=100&since=0'.format(id))
        if response.status_code == 200:
            json_format = response.json()
            player = json_format['player']
            id64 = player['steam']['id64']
            return id64    
        
    def get_banned(etf2l):
        split = etf2l.split('/')
        id = split[-2]
        response  = requests.get('https://api.etf2l.org/player/{}.json?per_page=100&since=0'.format(id))
        if response.status_code == 200:
            json_format = response.json()
            player = json_format['player']
            bans = player['bans']
            
            banned = False
            if bans != None:
                for ban in bans:
                    # if time since ban > current time
                    if ban['end'] > int(time.time()):
                        banned = True
            print(banned)
            return banned
