import pandas as pd
import os

def add_team_result(teams, df, i, team, home):
    if not team in teams:
        teams[team] = {
            'P': [],
            'G_F': [],
            'G_A': [],
            'S_F': [],
            'S_A': [],
            'ST_F': [],
            'ST_A': [],
            'C_F': [],
            'C_A': []
        }
    ha = 'H' if home else 'A'

    if (len(teams[team]['P']) < 5):
        df.at[i,'enough_games'] = 0
    df.at[i,'form_'+ha] = 0.5 if len(teams[team]['P']) == 0 else sum(teams[team]['P'])/float(len(teams[team]['P']))
    df.at[i,'g_'+ha] = sum(teams[team]['G_F']) - sum(teams[team]['G_A'])
    df.at[i,'s_'+ha] = sum(teams[team]['S_F']) - sum(teams[team]['S_A'])
    df.at[i,'st_'+ha] = sum(teams[team]['ST_F']) - sum(teams[team]['ST_A'])
    df.at[i,'c_'+ha] = sum(teams[team]['C_F']) - sum(teams[team]['C_A'])

    teams[team]['P'].append(1.0 if ha == df.at[i,'FTR'] else (0.5 if df.at[i,'FTR'] == 'D' else 0.0))
    teams[team]['G_F'].append(df.at[i,'FT'+ha+'G'])
    teams[team]['G_A'].append(df.at[i,'FT'+('A' if home else 'H')+'G'])
    teams[team]['S_F'].append(df.at[i,ha+'S'])
    teams[team]['S_A'].append(df.at[i,('A' if home else 'H')+'S'])
    teams[team]['ST_F'].append(df.at[i,ha+'ST'])
    teams[team]['ST_A'].append(df.at[i,('A' if home else 'H')+'ST'])
    teams[team]['C_F'].append(df.at[i,ha+'C'])
    teams[team]['C_A'].append(df.at[i,('A' if home else 'H')+'C'])

    if len(teams[team]['P']) > 5:
        for key in teams[team]:
            teams[team][key] = teams[team][key][1:6]
    return teams, df

def read_season(filename):

    df = pd.read_csv('Data/'+filename+'.csv')

    # add columns giving input about form to dataframe
    df['year'] = filename[4:6]
    df['enough_games'] = 1
    df['form_H'] = 0.0
    df['form_A'] = 0.0
    df['g_H'] = 0
    df['g_A'] = 0
    df['s_H'] = 0
    df['s_A'] = 0
    df['st_H'] = 0
    df['st_A'] = 0
    df['c_H'] = 0
    df['c_A'] = 0

    teams = {}

    for i, row in df.iterrows():
        teams, df = add_team_result(teams, df, i, row['HomeTeam'],True)
        teams, df = add_team_result(teams, df, i, row['AwayTeam'],False)

    df_new = df[['Div', 'year', 'HomeTeam', 'AwayTeam', 'enough_games', 'FTR', 'form_H', 'form_A', 'g_H', 'g_A', 's_H', 's_A', 'st_H', 'st_A', 'c_H', 'c_A', 'B365H', 'B365D', 'B365A']]

    df_new.to_csv('game_data.csv', index=False, mode='a', header=not os.path.exists('game_data.csv'))

if os.path.isfile('game_data.csv'):
    os.remove('game_data.csv')

filenames = [
    'PL1011', 'PL1112', 'PL1213', 'PL1314', 'PL1415', 'PL1516', 'PL1617', 'PL1718', 'PL1819', 'PL1920', 'PL2021', 'PL2122',
    'BL1011', 'BL1112', 'BL1213', 'BL1314', 'BL1415', 'BL1516', 'BL1617', 'BL1718', 'BL1819', 'BL1920', 'BL2021', 'BL2122',
    'SA1011', 'SA1112', 'SA1213', 'SA1314', 'SA1415', 'SA1516', 'SA1617', 'SA1718', 'SA1819', 'SA1920', 'SA2021', 'SA2122',
    'PD1011', 'PD1112', 'PD1213', 'PD1314', 'PD1415', 'PD1516', 'PD1617', 'PD1718', 'PD1819', 'PD1920', 'PD2021', 'PD2122',
    'LC1011', 'LC1112', 'LC1213', 'LC1314', 'LC1415', 'LC1516', 'LC1617', 'LC1718', 'LC1819', 'LC1920', 'LC2021', 'LC2122'
    ]

for filename in filenames:
    read_season(filename)