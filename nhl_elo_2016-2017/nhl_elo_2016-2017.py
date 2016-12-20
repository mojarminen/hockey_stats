# -*- coding: utf-8 -*-

import math
import csv
import sys
import os

sys.path.append(os.path.abspath(".")) 
import history

# rankings based on season 2015-2016
teams = {'Dallas Stars': 101,
         'St.Louis Blues': 94,
         'Chicago Blackhawks': 92,
         'Anaheim Ducks': 96,
         'Los Angeles Kings': 88,
         'San Jose Sharks': 89,
         'Nashville Predators': 90,
         'Minnesota Wild': 83,
         'Colorado Avalanche': 76,
         'Arizona Coyotes': 72,
         'Winnipeg Jets': 72,
         'Calgary Flames': 66,
         'Vancouver Canucks': 66,
         'Edmonton Oilers': 59,
         'Washington Capitals': 109,
         'Pittsburgh Penguins': 94,
         'Florida Panthers': 95,
         'New York Rangers': 94,
         'New York Islanders': 89,
         'Tampa Bay Lightning': 87,
         'Philadelphia Flyers': 83,
         'Detroit Red Wings': 82,
         'Boston Bruins': 84,
         'Carolina Hurricanes': 76,
         'Ottawa Senators': 73,
         'New Jersey Devils': 73,
         'Montreal Canadiens': 74,
         'Buffalo Sabres': 75,
         'Columbus Blue Jackets': 68,
         'Toronto Maple Leafs': 60}

def get_updated_elos(home_goals, away_goals, home_rating, away_rating, home_benefit=0.07):
    WIN_SCORE = 1.
    DRAW_SCORE = 0.5
    LOSS_SCORE = 0.

    # These define the velocity of the changes. (currently best: K0=5, LAMBDA=0)
    K0 = 10
    LAMBDA = 0.1

    # These define the scale. (C=2, D=40 are currently the best found)
    C = 2.
    D = 40.

    estimated_home_score = 1/(1+math.pow(C, (away_rating-home_rating)/D)) + home_benefit
    if estimated_home_score > 1:
        estimated_home_score = 0.99
    estimated_away_score = 1 - estimated_home_score
#    print 'estimations:', estimated_home_score, '-', estimated_away_score

    home_score = LOSS_SCORE
    if home_goals > away_goals:
        home_score = WIN_SCORE
    elif home_goals == away_goals:
        home_score = DRAW_SCORE
    
    away_score = WIN_SCORE - home_score
    
    k = K0*pow((1+abs(home_goals-away_goals)), LAMBDA)
    return (int(round(home_rating + k*(home_score-estimated_home_score))),
            int(round(away_rating + k*(away_score-estimated_away_score))))


def print_rankings(elos):
    rankings = list(reversed(sorted(elos.items(), key=lambda x: x[1])))
    for idx, r in enumerate(rankings):
        print '%2s. %-15s %s' % (idx+1, r[0], r[1])
    

if __name__ == '__main__':
    # initial rankings
    print_rankings(teams)
    print
    
    # edit with pre-season games

    with open('/home/mikkoarminen/Desktop/betting/hockey_database/nhl_elo_2016-2017/nhl_preseason_2016-2017.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(csvreader):
            
            home_team, away_team = row[0].split(' - ')
            
            if row[1] == 'POSTP.':
                continue
            elif 'ET' in row[1] or 'pen.' in row[1]:
                goals, _ = row[1].split(' ')
                home_goals = min([int(x) for x in goals.split(':')])
                away_goals = home_goals
            else:
                home_goals, away_goals = [int(x) for x in row[1].split(':')]
                
            home_new, away_new = get_updated_elos(home_goals, away_goals, teams[home_team], teams[away_team])
            teams[home_team] = home_new
            teams[away_team] = away_new

    # season 2016-2017 matches

    matches = history.get_matches(league='NHL', season='2016-2017')
    matches = list(sorted(matches, key=lambda x: x['date']))
    
    for m in matches:        
        home_team = m['home_team']
        away_team = m['away_team']
        
        if home_team == 'St. Louis Blues':
            home_team = 'St.Louis Blues'
        if away_team == 'St. Louis Blues':
            away_team = 'St.Louis Blues'
        
        home_new, away_new = get_updated_elos(m['full_time_home_team_goals'], m['full_time_away_team_goals'], teams[home_team], teams[away_team])
        teams[home_team] = home_new
        teams[away_team] = away_new
    
    # rankings before main season
    print_rankings(teams)
