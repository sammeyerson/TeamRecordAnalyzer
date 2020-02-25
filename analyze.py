import csv
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from findRecord import findRecord
from findRecord import get_team_misc, get_game_logs, get_stats, \
get_single_season_stats, get_team_stats, get_opp_stats, get_schedule, \
get_team_schedule, record_with_player, record_without_player
from PastData.odds_analysis import excel_to_csv, odds_parser

start_date='2019-10-22'
end_date='2020-04-15'
#excel_to_csv()
odds_data=pd.read_csv('PastData/odds_hisotry.csv')
odds_parser(odds_data)

#print('Record without player: ',winCount,'-',lossCount)
#print('PPG without player: ', pointsAgainst/itt)
#print(findRecord('Lakers'))
#print(get_team_misc('MIA', 2020))

#print(get_single_season_stats('James Harden'))
#print(get_team_stats('MIA',2020))
#print(get_opp_stats('MIA',2020))


#print(get_game_logs('LaMarcus Aldridge',start_date,end_date))
#print(get_team_schedule('Spurs',2020))

"""
player=input('Enter Player Name(ie: James Harden, LeBron James):')
team=input('Enter Name of Team(Rockets for James Harden, Lakers for LeBron James):')

print('Record with ',player,': ',record_with_player(player, team))
print('Record without ',player,': ',record_without_player(player, team))
"""
