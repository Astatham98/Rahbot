import requests
from collections import Counter
from time import sleep


class Etf2l():
      def get_div(self, etf2l, sixes=True):
        split = etf2l.split('/')
        id = split[-2]
        gamemode = '6on6' if sixes else 'highlander'

        response  = requests.get('https://api.etf2l.org/player/{}/results.json?since=0'.format(id))
        
        if response.status_code == 200:
            json_format = response.json()
            competitions = json_format['results']
            divs = "Open"
            try:
                for c in competitions:
                    comp = c['competition']
                    print(gamemode, c['competition'])
                    if comp['type'] == gamemode and c['merced'] == 0:
                        if c['division']['name'] is not None:
                            divs = c['division']['name']
                            break
            except TypeError:
                divs = 'Open'
            
            print(divs)
            divs = divs[:-1] if divs[-2].isdigit() else divs
            
            ender = gamemode if gamemode != '6on6' else "6's"
            return 'Etf2l - ' + divs + ' ' + ender


