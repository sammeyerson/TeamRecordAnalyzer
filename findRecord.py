import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def findRecord(team):

    totalTeamData=pd.read_csv('TeamRecords/AllTeamsInfo.csv')
    winningPcts=[]
    teams=[]
    Rank=[]
    #teams=totalTeamData[['Team']]
    #print(teams)
    rowCount=totalTeamData.shape[0]
    itt=int(0)
    for i in range(rowCount):
        row=totalTeamData.iloc[itt]
        record=row['Overall']
        totals=record.split('-')
        teams.append(row['Team'])
        win=int(totals[0])
        loss=int(totals[1])
        winPercentage=float(win/(win+loss))
        winningPcts.append(winPercentage)

        #print('winPerc: ',winPercentage)
        #print(totals)
        itt=itt+1
        Rank.append(itt)

    #print(winningPcts)
    dataForDF={
    'Team' :teams,
    'Winning Pct':winningPcts
    }
    #print(teams)
    #print(winningPcts)
    #print(Rank)

    winPct_frame=pd.DataFrame(
    dataForDF,
    index=Rank)
    itt=int(0)
    print(winPct_frame)

    for i in range(rowCount):
        row=winPct_frame.iloc[itt]
        teamName=str(row['Team'])
        if team in teamName:
            return row['Winning Pct']

        itt=itt+1

    return winPct_frame


def strengthOfSchedule(team):

    




    return 0
