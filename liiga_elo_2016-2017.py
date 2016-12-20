# -*- coding: utf-8 -*-

import math

import history

# Initialize with 2015-2016 regular season full time results.
# teams[teamname] = (wins, draws, losses)
season_2015_2016 = {'HIFK':    (37, 10, 13),
                    u'Kärpät': (33, 14, 13),
                    'Tappara': (26, 20, 14),
                    'JYP':     (29, 12, 19),
                    'SaiPa':   (27, 13, 20),
                    'Lukko':   (24, 13, 23),
                    'TPS':     (23, 15, 22),
                    'KalPa':   (21, 17, 22),
                    'Pelicans':(24, 11, 25),
                    'Sport':   (20, 16, 24),
                    'KooKoo':  (16, 20, 24),
                    u'Ässät':  (20, 12, 28),
                    'HPK':     (18,  9, 33),
                    'Ilves':   (16, 10, 34),
                    'Jukurit':   (13, 14, 33)} # Blues replaced with Jukurit

elos = {}
for k,v in season_2015_2016.items():
    elos[k] = v[0]*2 + v[1]

'''
# Scale the values so that the middle value in sorted list is 1000.
middle_value = sorted(elos.values())[len(elos.values())/2]
scale_factor = 1000 / middle_value
for k in elos:
    elos[k] *= scale_factor
'''

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
    print_rankings(elos)

    print
    print 'updating...'
    print
        
    matches = history.get_matches(league='SM-LIIGA', season='2016-2017')
    matches = list(sorted(matches, key=lambda x: x['date']))
    
    for m in matches:
        home_new, away_new = get_updated_elos(m['full_time_home_team_goals'], m['full_time_away_team_goals'], elos[m['home_team']], elos[m['away_team']])
        elos[m['home_team']] = home_new
        elos[m['away_team']] = away_new
    
    print_rankings(elos)
    
