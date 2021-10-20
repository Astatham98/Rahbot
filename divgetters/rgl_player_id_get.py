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

        doc = requests.get(link).text
        soup = BeautifulSoup(doc, 'lxml')

        div_table = None

        for table in soup.find_all('table', class_='table table-striped'):
            row = table.select('tr')[1]
            if row.a and row.a.text.strip().startswith('Sixes S'):
                div_table = table
                break

        if not div_table: return 'Newcomer'

        best_div = 'Newcomer'

        for row in div_table.find_all('tr')[1:]:
            current_div = row.select('a')[1].text.strip()
            if divisions.get(current_div, len(divisions)) < divisions.get(best_div):
                best_div = current_div

        return ["RGL - " + best_div + " 6's"]

