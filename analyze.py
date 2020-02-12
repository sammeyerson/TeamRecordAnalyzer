import csv
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

teamdata=pd.read_csv('TeamRecords/NetsRecordInfo.csv')
playerdata=pd.read_csv('PlayerInfo/Kyrie.csv')
teamdf=teamdata.iloc[:,7:14]
#print(teamdf)
#print(playerdata)
teamGames=teamdata[['G','result','Tm','Opp']]
gamesPlayed=playerdata[['Rk','G']]
gamesPlayed=gamesPlayed[gamesPlayed['G']>0]
print(gamesPlayed)
print(teamGames)
