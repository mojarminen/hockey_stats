# -*- coding: utf-8 -*-

import math

import history
import db
import betting_strategy

INITIAL_MONEY = 1000

INITIAL_RATING = 1000
WIN_SCORE = 1
DRAW_SCORE = 0.5
LOSS_SCORE = 0

LEAGUE = 'KHL'
START = '1900-01-01'

# These define the scale.
c = 10
d = 400

# These should be selected appropriately.
#k = 20
k0 = 10
lmbd = 1
home_win_multiplier = 0.05 # small decimal number
max_draw_extra = 0.10
close_match_threshold = 20 # MIN_RATING-MAX_RATING
high_difference_threshold = 30 # MIN_RATING-MAX_RATING
draw_diminisher = 0.05

matches = history.get_matches(team=None, league=LEAGUE, season=None, start=START, end=None, cancelled=False, awarded=False)
elo_ratings = {}

tmp = history.get_full_time_1X2_percentages(league=LEAGUE)
common_1X2_percentages = {'1': tmp[0], 'X': tmp[1], '2': tmp[2]}

money = INITIAL_MONEY

for match in matches:
    home_team = match['home_team']
    away_team = match['away_team']
    home_goals = match['full_time_home_team_goals']
    away_goals = match['full_time_away_team_goals']
    
    print home_team, '-', away_team
    
    if home_team not in elo_ratings:
        if len(elo_ratings) == 0:
            elo_ratings[home_team] = INITIAL_RATING
        else:
            elo_ratings[home_team] = sum(elo_ratings.values())/len(elo_ratings)
        
    if away_team not in elo_ratings:
        if len(elo_ratings) == 0:
            elo_ratings[away_team] = INITIAL_RATING
        else:
            elo_ratings[away_team] = sum(elo_ratings.values())/len(elo_ratings)

    home_rating = elo_ratings[home_team]
    away_rating = elo_ratings[away_team]

    # Make estimations with the ELO ratings.
    
    estimated_home_score = 1/(1+math.pow(c, (away_rating-home_rating)/d))
    estimated_away_score = 1 - estimated_home_score
    
    x = home_rating - away_rating

    # TODO: how to get the extra to be given
    # max win_extra = common_1X2_percentages['2']
    # min win_extra = -common_1X2_percentages['1']
    if x > 0:
        win_extra = (1-away_rating/home_rating)*common_1X2_percentages['2']
    else:
        win_extra = -1 * (1-home_rating/away_rating)*common_1X2_percentages['1']
        
    home_win_probability = common_1X2_percentages['1'] + win_extra
    away_win_probability = common_1X2_percentages['2'] - win_extra
    draw_probability = common_1X2_percentages['X']

    assert home_win_probability + draw_probability + away_win_probability > 0.99
    assert home_win_probability + draw_probability + away_win_probability < 1.01
    assert home_win_probability > 0
    assert draw_probability > 0
    assert away_win_probability > 0

    if abs(x) < close_match_threshold:
        # close match => draw is more probable
        if home_rating > away_rating:
            draw_extra = max_draw_extra * away_rating/home_rating
        else:
            draw_extra = max_draw_extra * home_rating/away_rating
        print 'draw_extra:', draw_extra
        
        draw_probability += draw_extra
        print 'home_win_probability:', home_win_probability
        print 'removed from home_win_probability:', draw_extra*(home_win_probability/(home_win_probability+away_win_probability))
        new_home_win_probability = home_win_probability - draw_extra*(home_win_probability/(home_win_probability+away_win_probability))
        print 'removed from away_win_probability:', draw_extra*(away_win_probability/(home_win_probability+away_win_probability))
        new_away_win_probability = away_win_probability - draw_extra*(away_win_probability/(home_win_probability+away_win_probability))
    
        home_win_probability = new_home_win_probability
        away_win_probability = new_away_win_probability
    elif abs(x) > high_difference_threshold:
        # bigger difference => draw is less probable
        if home_rating > away_rating:
            draw_diminish = (1-away_rating/home_rating)*draw_probability
        else:
            draw_diminish = (1-home_rating/away_rating)*draw_probability
        print 'draw_diminish:', draw_diminish

        draw_probability -= draw_diminish
        new_home_win_probability = home_win_probability + (home_win_probability/(home_win_probability+away_win_probability))*draw_diminish
        new_away_win_probability = away_win_probability + (away_win_probability/(home_win_probability+away_win_probability))*draw_diminish

        home_win_probability = new_home_win_probability
        away_win_probability = new_away_win_probability
    
    assert home_win_probability + draw_probability + away_win_probability > 0.99
    assert home_win_probability + draw_probability + away_win_probability < 1.01
    
    print home_win_probability, draw_probability, away_win_probability
    print 1/home_win_probability, 1/draw_probability, 1/away_win_probability
    
    # Make bets.
    
    print 'making bets'

    # Get 1X2 odds.
    odds = db.get_match_1X2_odds(match['match_id'])['HIGHEST']
    
    bet_1, bet_X, bet_2 = betting_strategy.div_100(money, home_win_probability, odds['home_win'], draw_probability, odds['draw'], away_win_probability, odds['away_win'])
    money = money - bet_1 - bet_X - bet_2
    
    # Check result.

    # Collect.
    if match['full_time_home_team_goals'] > match['full_time_away_team_goals'] and bet_1:
        money += (odds['home_win'] * bet_1)
    elif match['full_time_home_team_goals'] < match['full_time_away_team_goals'] and bet_2:
        money += (odds['away_win'] * bet_2)
    elif match['full_time_home_team_goals'] == match['full_time_away_team_goals'] and bet_X:
        money += (odds['draw'] * bet_X)

    # Update ELO ratings.
    
    home_score = LOSS_SCORE
    if home_goals > away_goals:
        home_score = WIN_SCORE
    elif home_goals == away_goals:
        home_score = DRAW_SCORE
    
    away_score = WIN_SCORE - home_score
    
    k = k0*pow((1+abs(home_goals-away_goals)), lmbd)
    elo_ratings[home_team] += (k*(home_score-estimated_home_score))
    elo_ratings[away_team] += (k*(away_score-estimated_away_score))

print money
