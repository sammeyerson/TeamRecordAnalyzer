import csv
import pandas as pd
import numpy as np
import math

def excel_to_csv():

    #odds_hisotry= pd.read_excel(r'/Users/SamMeyerson 1/Downloads/nba_odds_2019-20.xlsx', sheet_name='Sheet1')
    odds_hisotry=pd.read_csv('PastData/odds_hisotry.csv')
    #odds_hisotry.to_csv(r'PastData/odds_hisotry.csv',index = None, header=True)
    #^source for data: https://www.sportsbookreviewsonline.com/scoresoddsarchives/nba/nbaoddsarchives.htm


    return 0



def home_favorites(data, marginOfVictory):


    #print(data)
    home_favorite_cover=[]
    for index, row in data.iterrows():

        if str(row['Home Moneyline'])[:1]=='-':
            spread  = str(row['Home Spread'])[1:]
            if spread== 'pk' or spread=='PK':
                spread=0
            home_diff=int(row['Home Score'])-int(row['Away Score'])


            if float(spread)>marginOfVictory:
                #print('Spread:: ', spread, '  Diff:: ', home_diff)
                if float(home_diff)>=float(spread):
                    home_favorite_cover.append('Yes')
                else:
                    home_favorite_cover.append('No')
    coveredCount=0
    notCoveredCount=0
    for x in home_favorite_cover:
        if x=='Yes':
            coveredCount+=1
        else:
            notCoveredCount+=1

    coveredRecord=str(coveredCount)+'-'+str(notCoveredCount)






    return coveredRecord

def odds_parser(odds_hisotry):
    #print(odds_hisotry)
    #create data frame that holds each team in game, date of game, final score, open/close
    #spread, ML, total
    home_team=[]
    home_score=[]
    away_team=[]
    away_score=[]
    date=[]
    open_spread=[]
    open_total=[]
    closed_spread=[]
    home_spreads=[]
    away_spreads=[]
    closed_total=[]
    V_ML=[]
    H_ML=[]
    Rank=[]
    itt=int(0)

    for index, row in odds_hisotry.iterrows():
        if str(row['VH'])=='V':

            formatted_date=str(row['Date'])
            formatted_date=formatted_date[:-2]+'-'+formatted_date[-2:]
            if len(formatted_date)==4:
                formatted_date='0'+formatted_date

            #date.append(str(row['Date']))
            date.append(formatted_date)

            team_name=str(row['Team'])
            if team_name[:2]=='LA':
                team_name=team_name[:2]+' '+team_name[2:]
            else:
                upper=0
                itter=int(0)
                for x in team_name:

                    if x.isupper():
                        upper=upper+1

                    if upper==2:
                        team_name=team_name[:itter]+' '+team_name[itter:]
                        break
                    itter+=1



            away_team.append(team_name)

            away_score.append(str(row['Final']))
            V_ML.append(int(row['ML']))

            if str(row['Close'])=='pk' or str(row['Close'])=='PK':
                #open_total.append(str(row['Open']))
                #closed_spread.append(str(row['Close']))
                spread=str('0')
                if int(row['ML'])<0:
                    home_spread='+'+str(row['Close'])
                    away_spread='-'+str(row['Close'])
                else:
                    home_spread='-'+str(row['Close'])
                    away_spread='+'+str(row['Close'])

                closed_spread.append(spread)
                home_spreads.append(home_spread)
                away_spreads.append(away_spread)
            else:

                if float(row['Close'])>45:
                    #open_total.append(str(row['Open']))
                    closed_total.append(str(row['Close']))
                else:
                    #open_spread.append(str(row['Open']))
                    #closed_spread.append(str(row['Close']))
                    spread=str('0')
                    if int(row['ML'])<0:
                        home_spread='+'+str(row['Close'])
                        away_spread='-'+str(row['Close'])
                    else:
                        home_spread='-'+str(row['Close'])
                        away_spread='+'+str(row['Close'])

                    closed_spread.append(spread)
                    home_spreads.append(home_spread)
                    away_spreads.append(away_spread)


        elif str(row['VH'])=='H':


            team_name=str(row['Team'])
            if team_name[:2]=='LA':
                team_name=team_name[:2]+' '+team_name[2:]
            else:
                upper=0
                itter=int(0)
                for x in team_name:

                    if x.isupper():
                        upper=upper+1

                    if upper==2:
                        team_name=team_name[:itter]+' '+team_name[itter:]
                        break
                    itter+=1


            home_team.append(team_name)

            home_score.append(str(row['Final']))
            H_ML.append(int(row['ML']))

            #if type(row['Open']) is float:
            if str(row['Close'])=='pk' or str(row['Close'])=='PK':
                #open_total.append(str(row['Open']))
                #closed_spread.append(str(row['Close']))
                spread=str('0')

                if int(row['ML'])<0:
                    home_spread='-'+str(row['Close'])
                    away_spread='+'+str(row['Close'])
                else:
                    home_spread='+'+str(row['Close'])
                    away_spread='-'+str(row['Close'])

                closed_spread.append(spread)
                home_spreads.append(home_spread)
                away_spreads.append(away_spread)
            else:

                if float(row['Close'])>45:
                    #open_total.append(str(row['Open']))
                    closed_total.append(str(row['Close']))
                else:
                    #open_spread.append(str(row['Open']))
                    #closed_spread.append(str(row['Close']))
                    spread=str('0')
                    if int(row['ML'])<0:
                        home_spread='-'+str(row['Close'])
                        away_spread='+'+str(row['Close'])
                    else:
                        home_spread='+'+str(row['Close'])
                        away_spread='-'+str(row['Close'])

                    closed_spread.append(spread)
                    home_spreads.append(home_spread)
                    away_spreads.append(away_spread)
        itt=itt+1
        Rank.append(itt)




    #C = A[len(A)//2:]
    Rank=Rank[len(Rank)//2:]
    #a = [x - 13 for x in a] 819
    Rank = [x - 818 for x in Rank]




    dataForDF={
    'Date':date,
    'Home Team': home_team,
    'Home Score':home_score,
    'Home Moneyline':H_ML,
    'Home Spread': home_spreads,
    'Away Team':away_team,
    'Away Score': away_score,
    'Away Moneyline':V_ML,
    'Away Spread':away_spreads,
    'Closed Total': closed_total
    }
    lineup_frame=pd.DataFrame(
    dataForDF,
    index=Rank)

    #datesIWannaSee=lineup_frame[lineup_frame['Date']=='1-03']
    #print(lineup_frame)
    #print(datesIWannaSee)

    return lineup_frame
