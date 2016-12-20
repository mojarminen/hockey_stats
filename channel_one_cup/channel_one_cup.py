# -*- coding: utf-8 -*-

import os
import os.path
import csv
import datetime
import sqlite3
import numpy
import math

DATAFILE = 'channel_one_cup_2003-2015.csv'

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
                penalties_home_goals = extra_time_home_goals
                penalties_away_goals = extra_time_away_goals
            elif 'pen.' in row[1]:
                penalties_home_goals, penalties_away_goals = [int(goals) for goals in row[1].split(' ')[0].split(':')]
                full_time_home_goals = min(penalties_home_goals, penalties_away_goals)              
                full_time_away_goals = min(penalties_home_goals, penalties_away_goals)              
                extra_time_home_goals = min(penalties_home_goals, penalties_away_goals)              
                extra_time_away_goals = min(penalties_home_goals, penalties_away_goals)              
            else:
                full_time_home_goals, full_time_away_goals = [int(goals) for goals in row[1].split(':')]
                extra_time_home_goals = full_time_home_goals              
                extra_time_away_goals = full_time_away_goals              
                penalties_home_goals = full_time_home_goals
                penalties_away_goals = full_time_away_goals
            
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


def get_homeaway_of_team(team, games):
    wins = 0
    losses = 0
    
    for g in games:
        if g['home_team'] == team:
            if g['penalties_home_goals'] > g['penalties_away_goals']:
                wins += 1
            elif g['penalties_home_goals'] < g['penalties_away_goals']:
                losses += 1
            else:
                print g
                raise Exception('Nooooooooooo!!!!')
        elif g['away_team'] == team:
            if g['penalties_home_goals'] < g['penalties_away_goals']:
                wins += 1
            elif g['penalties_home_goals'] > g['penalties_away_goals']:
                losses += 1
            else:
                print g
                raise Exception('Nooooooooooo!!!!')
                
    game_count = float(wins + losses)
                
    return wins, losses, wins/game_count, losses/game_count


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


def get_homeaway_of_teams(team1, team2, games):
    counts = [0, 0]

    for g in games:
        if g['home_team'] == team1 and g['away_team'] == team2:
            if g['penalties_home_goals'] > g['penalties_away_goals']:
                counts[0] += 1
            elif g['penalties_home_goals'] < g['penalties_away_goals']:
                counts[1] += 1
            else:
                print g
                raise Exception('Nooooooooooo!!!!')
        elif g['home_team'] == team2 and g['away_team'] == team1:
            if g['penalties_home_goals'] < g['penalties_away_goals']:
                counts[0] += 1
            elif g['penalties_home_goals'] > g['penalties_away_goals']:
                counts[1] += 1
            else:
                print g
                raise Exception('Nooooooooooo!!!!')
    
    game_count = float(sum(counts))
    return counts, counts[0]/game_count, counts[1]/game_count


def get_1X2_estimation(team1, team2, games, adjust_draw_avg=False):
    ps_team1 = get_1X2_of_team(team1, games)[3:]
    ps_team2 = get_1X2_of_team(team2, games)[3:]

    home_win = (ps_team1[0]+ps_team2[2])/2
    draw = (ps_team1[1]+ps_team2[1])/2
    away_win = (ps_team1[2]+ps_team2[0])/2

    if adjust_draw_avg:
        p_draw = draw_percentage(games)
        delta = draw - p_draw
        
        draw = p_draw
        home_win += (delta/2)
        away_win += (delta/2)
    
    # check that probabilities sum up to 1
    assert abs((home_win + draw + away_win) - 1.0) < 0.01
    
    return home_win, draw, away_win 


def get_homeaway_estimation(team1, team2, games):
    ps_team1 = get_homeaway_of_team(team1, games)[2:]
    ps_team2 = get_homeaway_of_team(team2, games)[2:]

    home_win = (ps_team1[0]+ps_team2[1])/2
    away_win = (ps_team1[1]+ps_team2[0])/2

    # check that probabilities sum up to 1
    assert abs((home_win + away_win) - 1.0) < 0.01
    
    return home_win, away_win 


def draw_percentage(games):
    game_count = 0
    draw_count = 0
    for g in games:
        game_count += 1
        if g['full_time_home_goals'] == g['full_time_away_goals']:
            draw_count += 1

    return float(draw_count) / float(game_count)


def poisson(successes, successes_mean):
    return (pow(math.e, -successes_mean)*pow(successes_mean, successes))/math.factorial(successes)


def get_overunder_estimations(home_team, away_team, games):
    
    # Get home/away mean amount of goals
    mean_home_goals = 0
    mean_away_goals = 0
    for game in games:
        mean_home_goals += game['full_time_home_goals']
        mean_away_goals += game['full_time_away_goals']
    mean_home_goals = float(mean_home_goals) / len(games)
    mean_away_goals = float(mean_away_goals) / len(games)

    home_team_home_goals_for = 0
    home_team_home_goals_against = 0
    home_team_home_games = 0
    home_team_away_goals_for = 0
    home_team_away_goals_against = 0
    home_team_away_games = 0
    away_team_away_goals_for = 0
    away_team_away_goals_against = 0
    away_team_away_games = 0
    away_team_home_goals_for = 0
    away_team_home_goals_against = 0
    away_team_home_games = 0
    for game in games:
        if game['home_team'] == home_team:
            home_team_home_goals_for += game['full_time_home_goals']
            home_team_home_goals_against += game['full_time_away_goals']
            home_team_home_games += 1
        elif game['away_team'] == home_team:
            home_team_away_goals_for += game['full_time_away_goals']
            home_team_away_goals_against += game['full_time_home_goals']
            home_team_away_games += 1
            
        if game['away_team'] == away_team:
            away_team_away_goals_for += game['full_time_away_goals']
            away_team_away_goals_against += game['full_time_home_goals']
            away_team_away_games += 1
        elif game['home_team'] == away_team:
            away_team_home_goals_for += game['full_time_home_goals']
            away_team_home_goals_against += game['full_time_away_goals']
            away_team_home_games += 1

    home_team_home_attack = (float(home_team_home_goals_for) / home_team_home_games) / mean_home_goals
    home_team_home_defence = (float(home_team_home_goals_against) / home_team_home_games) / mean_away_goals
    home_team_away_attack = (float(home_team_away_goals_for) / home_team_away_games) / mean_away_goals
    home_team_away_defence = (float(home_team_away_goals_against) / home_team_away_games) / mean_home_goals
    
    away_team_away_attack = (float(away_team_away_goals_for) / away_team_away_games) / mean_away_goals
    away_team_away_defence = (float(away_team_away_goals_against) / away_team_away_games) / mean_home_goals
    away_team_home_attack = (float(away_team_home_goals_for) / away_team_home_games) / mean_home_goals
    away_team_home_defence = (float(away_team_home_goals_against) / away_team_home_games) / mean_away_goals

    estimated_home_goals = home_team_home_attack * home_team_away_attack * away_team_away_defence * away_team_home_defence * mean_home_goals
    estimated_away_goals = home_team_home_defence * home_team_away_defence * away_team_away_attack * away_team_away_attack * mean_away_goals

    ous = []
    for ou_value in numpy.arange(0, 12.5, 0.5):
        ou_prob = 0
        exact_match_prob = 0
        for h in range(int(round(ou_value))+1):
            for a in range(int(round(ou_value))+1):
                if h+a < int(round(ou_value)):
                    ou_prob += poisson(h, estimated_home_goals)*poisson(a, estimated_away_goals)
                elif h+a == int(ou_value):
                    exact_match_prob += poisson(h, estimated_home_goals)*poisson(a, estimated_away_goals)
        ous.append((ou_value, ou_prob, 1-ou_prob-exact_match_prob))
    return ous


if __name__ == '__main__':
    games = read_data(DATAFILE)

    print '***********'
    print '*** 1X2 ***'
    print '***********'
    print 
    
    print 'common draw percentage:', draw_percentage(games)
    print

    print 'Sweden:', get_1X2_of_team('Sweden', games)
    print 'Russia:', get_1X2_of_team('Russia', games)
    print 'Finland:', get_1X2_of_team('Finland', games)
    print 'Czech Republic:', get_1X2_of_team('Czech Republic', games)
    print

    print 'Based on previous games between the teams:'
    print 'FIN-CZE', get_1X2_of_teams('Finland', 'Czech Republic', games)
    print 'SWE-RUS:', get_1X2_of_teams('Sweden', 'Russia', games)
    print 'RUS-CZE', get_1X2_of_teams('Russia', 'Czech Republic', games)
    print 'FIN-SWE', get_1X2_of_teams('Finland', 'Sweden', games)
    print 'RUS-FIN', get_1X2_of_teams('Russia', 'Finland', games)
    print 'CZE-SWE', get_1X2_of_teams('Czech Republic', 'Sweden', games)
    print

    print 'Based on all previous games of the teams:'
    print 'FIN-CZE', get_1X2_estimation('Finland', 'Czech Republic', games, True)
    print 'SWE-RUS:', get_1X2_estimation('Sweden', 'Russia', games, True)
    print 'RUS-CZE', get_1X2_estimation('Russia', 'Czech Republic', games, True)
    print 'FIN-SWE', get_1X2_estimation('Finland', 'Sweden', games, True)
    print 'RUS-FIN', get_1X2_estimation('Russia', 'Finland', games, True)
    print 'CZE-SWE', get_1X2_estimation('Czech Republic', 'Sweden', games, True)
    print 
    
    print '*****************'
    print '*** Home/Away ***'
    print '*****************'
    print 
    
    print 'Sweden:', get_homeaway_of_team('Sweden', games)
    print 'Russia:', get_homeaway_of_team('Russia', games)
    print 'Finland:', get_homeaway_of_team('Finland', games)
    print 'Czech Republic:', get_homeaway_of_team('Czech Republic', games)
    print

    print 'Based on previous games between the teams:'
    probs = get_homeaway_of_teams('Finland', 'Czech Republic', games)
    print 'FIN-CZE', probs, (1/probs[1], 1/probs[2])
    probs = get_homeaway_of_teams('Sweden', 'Russia', games)
    print 'SWE-RUS:', probs, (1/probs[1], 1/probs[2]) 
    probs = get_homeaway_of_teams('Russia', 'Czech Republic', games)
    print 'RUS-CZE', probs, (1/probs[1], 1/probs[2])
    probs = get_homeaway_of_teams('Finland', 'Sweden', games)
    print 'FIN-SWE', probs, (1/probs[1], 1/probs[2])
    probs = get_homeaway_of_teams('Russia', 'Finland', games)
    print 'RUS-FIN', probs, (1/probs[1], 1/probs[2])
    probs = get_homeaway_of_teams('Czech Republic', 'Sweden', games)
    print 'CZE-SWE', probs, (1/probs[1], 1/probs[2])
    print

    print 'Based on all previous games of the teams:'
    probs = get_homeaway_estimation('Finland', 'Czech Republic', games)
    print 'FIN-CZE', probs, (1/probs[0], 1/probs[1])
    probs = get_homeaway_estimation('Sweden', 'Russia', games)
    print 'SWE-RUS:', probs, (1/probs[0], 1/probs[1]) 
    probs = get_homeaway_estimation('Russia', 'Czech Republic', games)
    print 'RUS-CZE', probs, (1/probs[0], 1/probs[1])
    probs = get_homeaway_estimation('Finland', 'Sweden', games)
    print 'FIN-SWE', probs, (1/probs[0], 1/probs[1])
    probs = get_homeaway_estimation('Russia', 'Finland', games)
    print 'RUS-FIN', probs, (1/probs[0], 1/probs[1])
    probs = get_homeaway_estimation('Czech Republic', 'Sweden', games)
    print 'CZE-SWE', probs, (1/probs[0], 1/probs[1])
    print 

    print '******************'
    print '*** Over/Under ***'
    print '******************'
    print
    
    print 'FIN-CZE:'
    for ou in get_overunder_estimations('Finland', 'Czech Republic', games):
        probs = [round(ou[1], 2), round(ou[2], 2)]
        print str(ou[0]) + ':', probs, (round(1/probs[0], 2) if probs[0] else 0.00, round(1/probs[1], 2) if probs[1] else 0.00) 
    print

    print 'SWE-RUS:'
    for ou in get_overunder_estimations('Sweden', 'Russia', games):
        probs = (round(ou[1], 2), round(ou[2], 2))
        print str(ou[0]) + ':', probs, (round(1/probs[0], 2) if probs[0] else 0.00, round(1/probs[1], 2) if probs[1] else 0.00) 
    print
