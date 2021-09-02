import requests
from collections import Counter
from time import sleep


class Etf2l():
      def get_div(self, etf2l):
        split = etf2l.split('/')
        id = split[-2]

        response  = requests.get('https://api.etf2l.org/player/{}/results.json?since=0'.format(id))
        
        if response.status_code == 200:
            json_format = response.json()
            competitions = json_format['results']
            divs = ""
            try:
                for c in competitions:
                    comp = c['competition']
                    if comp['type'] == '6on6' and c['merced'] == 0:
                        if c['division']['name'] is not None:
                            divs = c['division']['name']
                            break
            except TypeError:
                divs = 'Open'
            
            print(divs)
            #count = Counter(divs)
            #return 'Etf2l - ' + count.most_common()[0][0]
            return 'Etf2l - ' + divs


