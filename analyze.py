import csv
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scraper import findRecord
from scraper import get_team_misc, get_game_logs, get_stats, \
get_single_season_stats, get_team_stats, get_opp_stats, get_schedule, \
get_team_schedule, record_with_player, record_without_player
from PastData.odds_analysis import excel_to_csv, odds_parser, home_favorites, \
away_favorites, away_dogs, home_dogs
from box_scores import get_box_scores

try:
    from constants import TEAM_TO_TEAM_ABBR
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR


start_date='2019-10-22'
end_date='2020-04-15'
#excel_to_csv()
odds_data=pd.read_csv('PastData/odds_hisotry.csv')

data=odds_parser(odds_data)
#print(data)

#print('Home favorites ATS: ', home_favorites(data, 0))
#print('Away favorites ATS: ', away_favorites(data,0))
#print('Away dogs ATS: ', away_dogs(data, 0))
#print('Home dogs ATS: ', home_dogs(data, 0))
#print(odds_parser(odds_data))
#print(SOS('Lakers'))

#print('Record without player: ',winCount,'-',lossCount)
#print('PPG without player: ', pointsAgainst/itt)
#print(findRecord('Lakers'))
#print(get_team_misc('MIA', 2020))

#print(get_single_season_stats('James Harden'))
#print(get_team_stats('MIA',2020))
#print(get_opp_stats('MIA',2020))


#print(get_game_logs('LaMarcus Aldridge',start_date,end_date))
#print(get_team_schedule('Heat',2020))
dataFrameMiami=get_team_schedule('Heat',2020)
#print(dataFrameMiami)
dates=dataFrameMiami[['DATE','Team','Opponent']]
dates['Team'] = dates['Team'].str.upper()
dates['Team'] = dates['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
dates['Opponent'] = dates['Opponent'].str.upper()
dates['Opponent'] = dates['Opponent'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
print(dates)
for index, row in dates.iterrows():
    date=row['DATE']
    team=row['Team']
    opponent=row['Opponent']
    boxscore=get_box_scores(date,team,opponent)
    
    print(boxscore)





#player=input('Enter Player Name(ie: James Harden, LeBron James):')
#team=input('Enter Name of Team(Rockets for James Harden, Lakers for LeBron James):')

#print('Record with ',player,': ',record_with_player(player, team))
#print('Record without ',player,': ',record_without_player(player, team))
