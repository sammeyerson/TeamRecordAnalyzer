from requests import get
from bs4 import BeautifulSoup

def get_game_suffix(date, team1, team2):
    r = get(f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'class': 'teams'}):
            for anchor in table.find_all('a'):
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    return suffix

def get_player_suffix(name):
    names = name.split(' ')[1:]
    for last_name in names:
        initial = last_name[0].lower()
        r = get(f'https://www.basketball-reference.com/players/{initial}')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            for table in soup.find_all('table', attrs={'id': 'players'}):
                for anchor in table.find_all('a'):
                    if anchor.text==name:
                        suffix = anchor.attrs['href']
                        return suffix
