import requests
from bs4 import BeautifulSoup
import re


class Ozfortress:
    def get_div(self, user):
        league = user + "#leagues"
        doc = requests.get(league).text
        soup = BeautifulSoup(doc, "lxml")

        teams = soup.find_all(class_="list-group list-group-flush mb-4")
        teams = soup.find_all(class_="row ml-0") if not teams else teams
        for team in teams:
            if (
                "ultiduo" not in team.text.strip().lower()
                and "state v state" not in team.text.strip().lower()
            ):
                newest_team = team.text.strip()
                break

        try:
            league = re.findall(r" in (.*?) on ", newest_team)[0]
        except IndexError:
            league = re.findall(r" in (.*?) for ", newest_team)[0]
        new_league = self.convert_to_season_rank(league)
        return new_league

    def convert_to_season_rank(self, league):
        rank_dict = {
            "Division 1": "Premier",
            "Division 2": "Intermediate",
            "Division 3": "Main",
            "Division 4": "Open",
        }
        try:
            return ["Ozfortress - " + rank_dict[league] + " " + "6's"]
        except Exception:
            return ["Ozfortress - " + league + " " + "6's"]
