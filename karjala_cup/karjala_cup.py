# -*- coding: utf-8 -*-

import os
import os.path
import csv
import datetime
import sqlite3

DATAFILE = 'karjala_cup_2006-2015.csv'

def read_data(filepath):
    result = []
    with open(filepath, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            
            cancelled = False
            awarded = False
            full_time_home_goals = None
            full_time_away_goals = None
            extra_time_home_goals = None
            extra_time_away_goals = None
            penalties_home_goals = None
            penalties_away_goals = None
            
            # Jump over heading rows.
            if ('Round' in row[0] or row[0] == '') and row[2] == '1' and row[3] == 'X' and row[4] == '2':
                continue
            
            # parse teams
            home_team, away_team = row[0].split(' - ')
            assert len(home_team) > 0
            assert len(away_team) > 0

            # parse result
            if 'CAN.' in row[1]:
                cancelled = True
            elif 'AWA.' in row[1]:
                full_time_home_goals, full_time_away_goals = [int(goals) for goals in row[1].split(' ')[0].split(':')]                
                awarded = True
            elif 'ET' in row[1]:
                extra_time_home_goals, extra_time_away_goals = [int(goals) for goals in row[1].split(' ')[0].split(':')]
                full_time_home_goals = min(extra_time_home_goals, extra_time_away_goals)              
                full_time_away_goals = min(extra_time_home_goals, extra_time_away_goals)              
            elif 'pen.' in row[1]:
                penalties_home_goals, penalties_away_goals = [int(goals) for goals in row[1].split(' ')[0].split(':')]
                full_time_home_goals = min(penalties_home_goals, penalties_away_goals)              
                full_time_away_goals = min(penalties_home_goals, penalties_away_goals)              
                extra_time_home_goals = min(penalties_home_goals, penalties_away_goals)              
                extra_time_away_goals = min(penalties_home_goals, penalties_away_goals)              
            else:
                full_time_home_goals, full_time_away_goals = [int(goals) for goals in row[1].split(':')]
            
            # parse date
            day, month, year = [int(d) for d in row[5].split('.')]
            date = datetime.date(year, month, day).strftime('%Y-%m-%d')

            # parse odds
            home_win, draw, away_win = float(row[2] or '0'), float(row[3] or '0'), float(row[4] or '0')
            
            result.append({'date': date, 
                           'home_team': home_team, 
                           'away_team': away_team, 
                           'full_time_home_goals': full_time_home_goals, 
                           'full_time_away_goals': full_time_away_goals, 
                           'extra_time_home_goals': extra_time_home_goals, 
                           'extra_time_away_goals': extra_time_away_goals, 
                           'penalties_home_goals': penalties_home_goals, 
                           'penalties_away_goals': penalties_away_goals, 
                           'cancelled': cancelled, 
                           'awarded': awarded,
                           'home_win_odds': home_win,
                           'draw_odds': draw,
                           'away_win_odds': away_win})
                           
    return result

def get_1X2_of_team(team, games):
    wins = 0
    draws = 0
    losses = 0
    
    for g in games:
        if g['home_team'] == team:
            if g['full_time_home_goals'] > g['full_time_away_goals']:
                wins += 1
            elif g['full_time_home_goals'] < g['full_time_away_goals']:
                losses += 1
            else:
                draws += 1
        elif g['away_team'] == team:
            if g['full_time_home_goals'] < g['full_time_away_goals']:
                wins += 1
            elif g['full_time_home_goals'] > g['full_time_away_goals']:
                losses += 1
            else:
                draws += 1
                
    game_count = float(wins + draws + losses)
                
    return wins, draws, losses, wins/game_count, draws/game_count, losses/game_count


def get_1X2_of_teams(team1, team2, games):
    counts = [0, 0, 0]

    for g in games:
        if g['home_team'] == team1 and g['away_team'] == team2:
            if g['full_time_home_goals'] > g['full_time_away_goals']:
                counts[0] += 1
            elif g['full_time_home_goals'] < g['full_time_away_goals']:
                counts[2] += 1
            else:
                counts[1] += 1
        elif g['home_team'] == team2 and g['away_team'] == team1:
            if g['full_time_home_goals'] < g['full_time_away_goals']:
                counts[0] += 1
            elif g['full_time_home_goals'] > g['full_time_away_goals']:
                counts[2] += 1
            else:
                counts[1] += 1
    
    game_count = float(sum(counts))
    return counts, counts[0]/game_count, counts[1]/game_count, counts[2]/game_count


def draw_percentage(games):
    game_count = 0
    draw_count = 0
    for g in games:
        game_count += 1
        if g['full_time_home_goals'] == g['full_time_away_goals']:
            draw_count += 1

    return float(draw_count) / float(game_count)

if __name__ == '__main__':
    games = read_data(DATAFILE)
    
    print 'common draw percentage:', draw_percentage(games)

    print 'Sweden:', get_1X2_of_team('Sweden', games)
    print 'Russia:', get_1X2_of_team('Russia', games)
    print 'Finland:', get_1X2_of_team('Finland', games)
    print 'Czech Republic:', get_1X2_of_team('Czech Republic', games)

#    print get_1X2_of_teams('Finland', 'Sweden', games)
#    print get_1X2_of_teams('Sweden', 'Finland', games)
#    print get_1X2_of_teams('Finland', 'Russia', games)
    print 'SWE-RUS:', get_1X2_of_teams('Sweden', 'Russia', games)
    print 'FIN-CZE', get_1X2_of_teams('Finland', 'Czech Republic', games)
