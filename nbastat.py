from requests import get
from pprint import PrettyPrinter
import json

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()

def getLinks():
    nbaData = get(BASE_URL + ALL_JSON).json()
    links = nbaData['links']
    return links

def getScoreboard():
    scoreboard = getLinks()['currentScoreboard']
    games = get(BASE_URL + scoreboard).json()['games']

    for game in games:
        homeTeam = game['hTeam']
        awayTeam = game['vTeam']
        clock = game['clock']
        period = game['period']
        print("========================================") 
        print(f"{homeTeam['triCode']} vs {awayTeam['triCode']}")
        print(f"{homeTeam['score']} - {awayTeam['score']}")
        print(f"{clock} - {period['current']}")

def getStats():
    stats = getLinks()['leagueTeamStatsLeaders']
    teams = get(BASE_URL + stats).json()['league']['standard']['regularSeason']['teams']

    teams = list(filter(lambda x: x['name'] != "Team", teams))
    teams.sort(key = lambda x: int( x['ppg']['rank']))

    for i, team in enumerate(teams):
        teamName = team['name']
        nickname = team['nickname']
        ppg = team['ppg']['avg']
        print(f"{i+1}. {teamName}-{nickname}-{ppg}")


getStats()
