import csv
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from findRecord import findRecord

teamdata=pd.read_csv('TeamRecords/BucksRecordInfo.csv')
playerdata=pd.read_csv('PlayerInfo/Giannis.csv')
teamdf=teamdata.iloc[:,7:14]
#print(teamdf)
#print(playerdata)
teamGames=teamdata[['Rk','result','Tm','Opp']]

gamesPlayed=playerdata[['Rk','G']]
gamesPlayed.replace(to_replace=np.nan, value= 0)

gamesMissed=gamesPlayed[gamesPlayed['G'].isnull()]
gamesPlayed=gamesPlayed[gamesPlayed['G']>0]

#print(gamesPlayed)
#print(teamGames)

commonGames = pd.merge(teamGames, gamesPlayed, on=['Rk'], how='inner')
uncommonGames= pd.merge(teamGames, gamesMissed, on=['Rk'])
#print(commonGames)
itt=int(0)
winCount=int(0)
lossCount=int(0)

pointsFor=int(0)
pointsAgainst=int(0)
for index, row in commonGames.iterrows():

    if(row['result']=='W'):
        winCount=winCount+1

    else:
        lossCount=lossCount+1
    pointsFor=pointsFor+int(row['Tm'])
    itt=itt+1
print('Record with player: ',winCount,'-',lossCount)
print('PPG with player: ',pointsFor/itt)


#print(uncommonGames)
itt=int(0)
winCount=int(0)
lossCount=int(0)
for index, row in uncommonGames.iterrows():

    if(row['result']=='W'):
        winCount=winCount+1
    else:
        lossCount=lossCount+1
    pointsAgainst=pointsAgainst+int(row['Tm'])
    itt=itt+1
print('Record without player: ',winCount,'-',lossCount)
print('PPG without player: ', pointsAgainst/itt)
#print(findRecord('hi'))
