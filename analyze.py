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
teamGames=teamdata[['Rk','result','Tm','Opp']]
gamesPlayed=playerdata[['Rk','G']]
gamesPlayed=gamesPlayed[gamesPlayed['G']>0]
#print(gamesPlayed)
#print(teamGames)

commonGames = pd.merge(teamGames, gamesPlayed, on=['Rk'], how='inner')
print(commonGames)
itt=int(0)
winCount=int(0)
lossCount=int(0)
for index, row in commonGames.iterrows():

    if(row['result']=='W'):
        winCount=winCount+1
    else:
        lossCount=lossCount+1
    itt=itt+1
print(winCount,'-',lossCount)
