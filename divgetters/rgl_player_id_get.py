from bs4 import BeautifulSoup
import requests

#Evaluates a players division based on the highest division team they
#have played for. The main caveat here is that RGL displays teams on
#a players profile even if they have not competed in a match. This can
#be mitigated by checking on each respective teams page for payment, 
#though this adds extra computational overhead.

class RGL():
    def get_div(self, link):
        divisions = {
        "Invite": 1, 
        "Advanced": 2, 
        "Main": 3, 
        "Intermediate": 4, 
        "Amateur": 5, 
        "Newcomer": 6 
        }
        
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        }

        req = requests.Session()
        doc = req.get(link, headers=headers).text
        soup = BeautifulSoup(doc, 'lxml')

        div_table = []
        for gamemode in ['HL S', 'Sixes S']:
            for table in soup.find_all('table', class_='table table-striped'):
                row = table.select('tr')[1]
                if row.a and row.a.text.strip().startswith(gamemode):
                    div_table.append(table)
                    break

        if not div_table: return ["RGL - Newcomer 6s", "RGL - Newcomer highlander"]

        
        best_divs = []
        for table in div_table:
            best_div = 'Newcomer'
            for row in table.find_all('tr')[1:]:
                current_div = row.select('a')[1].text.strip()
                if divisions.get(current_div, len(divisions)) < divisions.get(best_div):
                    best_div = current_div
            best_divs.append(best_div)
        
        full_divs = []
        for i, gamemode in enumerate([" highlander", " 6s"]):
            if i+1 > len(best_divs):
                full_divs.append(f"RGL - {best_divs[0]}{gamemode}")
            else:
                full_divs.append(f"RGL - {best_divs[i]}{gamemode}")

        print(full_divs)
        return full_divs