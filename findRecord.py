import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR

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

    return 0


def strengthOfSchedule(team):






    return 0



def get_team_misc(team, season_end_year):
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div=div_misc_stats')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = list(map(lambda x: x[1], list(df.columns)))
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.rename(columns = {'Age': 'AGE', 'Pace': 'PACE', 'Arena': 'ARENA', 'Attend.': 'ATTENDANCE', 'Attend./G': 'ATTENDANCE/G'}, inplace=True)
        s = df[df['TEAM']==team]
        #s['SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])

def get_game_logs(name, start_date, end_date, playoffs=False):
    try:
        from utils import get_player_suffix
    except:
        from basketball_reference_scraper.utils import get_player_suffix

    suffix = get_player_suffix(name).replace('/', '%2F').replace('.html', '')
    start_date_str = start_date
    end_date_str = end_date
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    years = list(range(start_date.year, end_date.year+2))
    if playoffs:
        selector = 'div_pgl_basic_playoffs'
    else:
        selector = 'div_pgl_basic'
    final_df = None
    for year in years:
        r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}%2Fgamelog%2F{year}&div={selector}')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table')
            if table:
                df = pd.read_html(str(table))[0]
                df.rename(columns = {'Date': 'DATE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
                        'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE'}, inplace=True)
                df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
                df = df[df['Rk']!='Rk']
                df = df.drop(['Rk', 'G','Age'], axis=1)
                df = df.loc[(df['DATE'] >= start_date_str) & (df['DATE'] <= end_date_str)]
                active_df = pd.DataFrame(columns = list(df.columns))
                for index, row in df.iterrows():
                    #if len(row['GS'])>1:
                        #ontinue
                    active_df = active_df.append(row, sort=False)
                if final_df is None:
                    final_df = pd.DataFrame(columns=list(active_df.columns))
                final_df = final_df.append(active_df, sort=False)
    return final_df


def get_stats(name, stat_type='PER_GAME', playoffs=False, career=False):
    try:
        from utils import get_player_suffix
    except:
        from basketball_reference_scraper.utils import get_player_suffix
    suffix = get_player_suffix(name).replace('/', '%2F')
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                  'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
        career_index = df[df['SEASON']=='Career'].index[0]
        if career:
            df = df.iloc[career_index+2:, :]
        else:
            df = df.iloc[:career_index, :]

        df = df.reset_index().dropna(axis=1).drop('index', axis=1)
        return df

def get_single_season_stats(playerName, stat_type='PER_GAME'):

    careerStats=get_stats(playerName, stat_type)
    return careerStats.tail(1)

def get_team_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format=='TOTAL':
        selector = 'div_team-stats-base'
    elif data_format=='PER_GAME':
        selector = 'div_team-stats-per_game'
    elif data_format=='PER_POSS':
        selector = 'div_team-stats-per_poss'
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        s = df[df['TEAM']==team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])


def get_opp_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format=='TOTAL':
        selector = 'div_opponent-stats-base'
    elif data_format=='PER_GAME':
        selector = 'div_opponent-stats-per_game'
    elif data_format=='PER_POSS':
        selector = 'div_opponent-stats-per_poss'
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.columns = list(map(lambda x: 'OPP_'+x, list(df.columns)))
        df.rename(columns={'OPP_TEAM': 'TEAM'}, inplace=True)
        s = df[df['TEAM']==team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])

def get_schedule(season, playoffs=False):
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May']
    df = pd.DataFrame()
    for month in months:
        r = get(f'https://www.basketball-reference.com/leagues/NBA_{season}_games-{month.lower()}.html')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            month_df = pd.read_html(str(table))[0]
            df = df.append(month_df, sort=False)
    df = df.reset_index()
    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']
    playoff_loc = df[df['DATE']=='Playoffs']
    if len(playoff_loc.index)>0:
        playoff_index = playoff_loc.index[0]
    else:
        playoff_index = len(df)
    if playoffs:
        df = df[playoff_index+1:]
    else:
        df = df[:playoff_index]
    df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
    return df

def get_team_schedule(team, season ,playoffs=False):
    #MUST USE FULL TEAM NAME (ie 'Lakers' or 'Heat') NOT ABBREVIATION
    total_schedule=get_schedule(season)
    total_schedule=total_schedule[total_schedule['HOME_PTS']>0]
    total_schedule=total_schedule[total_schedule['VISITOR'].str.contains(team) | total_schedule['HOME'].str.contains(team)]
    #print(total_schedule)
    itt=int(0)
    teams=[]
    dates=[]
    opponent=[]
    points=[]
    opp_points=[]
    Rank=[]
    home_away=[]


    for index, row in total_schedule.iterrows():

        if team in str(row['HOME']) and float(row['HOME_PTS'])>0:
            teams.append(row['HOME'])
            dates.append(row['DATE'])
            opponent.append(row['VISITOR'])
            points.append(row['HOME_PTS'])
            opp_points.append(row['VISITOR_PTS'])
            home_away.append('Home')
            itt=itt+1
            Rank.append(itt)

        elif team in str(row['VISITOR']) and float(row['HOME_PTS'])>0:
            teams.append(row['VISITOR'])
            dates.append(row['DATE'])
            opponent.append(row['HOME'])
            points.append(row['VISITOR_PTS'])
            opp_points.append(row['HOME_PTS'])
            home_away.append('Away')
            itt=itt+1
            Rank.append(itt)

        if float(row['HOME_PTS'])<0:
            break




    dataForDF={
    'DATE':dates,
    'Team': teams,
    'Home/Away': home_away,
    'Points': points,
    'Opponent':opponent,
    'Opponent Points':opp_points

    }
    team_schedule=pd.DataFrame(
    dataForDF,
    index=Rank)



    return team_schedule

def record_with_player(player, team):

    start_date='2019-10-22'
    end_date='2020-04-15'
    player_game_log=get_game_logs(player,start_date,end_date)

    player_games_played=player_game_log[['DATE','3P']]

    player_games_played=player_games_played[player_games_played['3P']!='Inactive']
    player_games_played=player_games_played[player_games_played['3P']!='Did Not Play']

    player_games_played['DATE']=player_games_played['DATE'].astype(str)
    team_schedule=get_team_schedule(team,2020)
    team_schedule['DATE']=team_schedule['DATE'].astype(str)
    commonGames = pd.merge(player_games_played, team_schedule, on=['DATE'], how='inner', sort=True)
    winCount=0
    lossCount=0
    for index, row in commonGames.iterrows():
        if float(row['Points'])>float(row['Opponent Points']):
            winCount=winCount+1
        else:
            lossCount=lossCount+1
    recordWPlayer=str(winCount)+'-'+str(lossCount)
    return recordWPlayer

def record_without_player(player, team):

    start_date='2019-10-22'
    end_date='2020-04-15'
    player_game_log=get_game_logs(player,start_date,end_date)

    player_games_played=player_game_log[['DATE','3P']]
    date_game_missed=[]
    itt=int(0)
    Rank=[]

    for index, row in player_games_played.iterrows():
        if str(row['3P'])=='Inactive':
            date_game_missed.append(row['DATE'])
            itt=itt+1
            Rank.append(itt)
        elif str(row['3P'])=='Did Not Play':
            date_game_missed.append(row['DATE'])
            itt=itt+1
            Rank.append(itt)

    dataForDF={
    'DATE':date_game_missed,

    }
    player_games_missed=pd.DataFrame(
    dataForDF,
    index=Rank)

    player_games_missed['DATE']=player_games_missed['DATE'].astype(str)
    team_schedule=get_team_schedule(team,2020)
    team_schedule['DATE']=team_schedule['DATE'].astype(str)
    uncommonGames = pd.merge(player_games_missed, team_schedule, on=['DATE'], sort=False)
    winCount=0
    lossCount=0
    for index, row in uncommonGames.iterrows():
        if float(row['Points'])>float(row['Opponent Points']):
            winCount=winCount+1
        else:
            lossCount=lossCount+1
    recordWPlayer=str(winCount)+'-'+str(lossCount)
    return recordWPlayer
