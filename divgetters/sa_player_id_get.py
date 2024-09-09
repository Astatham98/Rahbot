import requests
from bs4 import BeautifulSoup
import re


class SA:
    def get_div(self, user):
        league = user + "#leagues"
        doc = requests.get(league).text
        soup = BeautifulSoup(doc, "lxml")

        teams = soup.find_all(class_="list-group list-group-flush mb-4")
        teams = soup.find_all(class_="row ml-0") if not teams else teams
        newest_team = ""
        for team in teams:
            if "ultiduo" not in team.text.strip().lower():
                newest_team = team.text.strip()
                break

        try:
            league = re.findall(r" in (.*?) on ", newest_team)[0]
        except IndexError:
            try:
                league = re.findall(r" in (.*?) for ", newest_team)[0]
            except IndexError:
                league = ""
        new_league = self.convert_to_season_rank(league)
        return new_league

    def convert_to_season_rank(self, league):
        divs = ["Elite", "Central", "Acesso", "Aberta", "Iniciante"]
        div = [x for x in divs if x.lower() in league.lower()]

        try:
            return ["FBTF - " + div[0] + " " + "6's"]
        except IndexError:
            return ["FBTF - " + "Iniciante" + " " + "6's"]
