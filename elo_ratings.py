# -*- coding: utf-8 -*-

import math
import random

import history
import db
import betting_strategy

# These define the scale.
C = 10.
D = 400.

INITIAL_RATING = 1000.

WIN_SCORE = 1.
DRAW_SCORE = 0.5
LOSS_SCORE = 0.


def main(league, first_match_date, money, class_difference, close_match_threshold, max_draw_extra, k0, lmbd):
    
    elo_ratings = {}
    def get_elo_rating(team):
        if team not in elo_ratings:
            elo_ratings[team] = INITIAL_RATING
        return elo_ratings[team]

    matches = history.get_matches(team=None, league=league, season=None, start=first_match_date, end=None, cancelled=False, awarded=False)

    tmp = history.get_full_time_1X2_percentages(league=LEAGUE)
    common_1X2_percentages = {'1': tmp[0], 'X': tmp[1], '2': tmp[2]}
        
    for idx, match in enumerate(matches):
        home_team = match['home_team']
        away_team = match['away_team']
        home_goals = match['full_time_home_team_goals']
        away_goals = match['full_time_away_team_goals']
        
#        print home_team, '-', away_team, ':', str(home_goals) + '-' + str(away_goals)
        
        home_rating = get_elo_rating(home_team)
        away_rating = get_elo_rating(away_team)

        # Make estimations with the ELO ratings.
        
        estimated_home_score = 1/(1+math.pow(C, (away_rating-home_rating)/D))
        estimated_away_score = 1 - estimated_home_score
        
        if home_rating - away_rating > 0:
            win_extra = ((home_rating - away_rating)/class_difference)*0.01
            win_extra = min(win_extra, 1-common_1X2_percentages['X']-common_1X2_percentages['2'])

            home_win_probability = common_1X2_percentages['1'] + win_extra
            away_win_probability = common_1X2_percentages['2'] - win_extra*common_1X2_percentages['2']/(common_1X2_percentages['X']+common_1X2_percentages['2'])
            draw_probability = common_1X2_percentages['X'] - win_extra*common_1X2_percentages['X']/(common_1X2_percentages['X']+common_1X2_percentages['2'])
        else:
            win_extra = ((away_rating - home_rating)/class_difference)*0.01
            win_extra = min(win_extra, 1-common_1X2_percentages['1']-common_1X2_percentages['X'])
            
            away_win_probability = common_1X2_percentages['2'] + win_extra
            home_win_probability = common_1X2_percentages['1'] - win_extra*common_1X2_percentages['1']/(common_1X2_percentages['1']+common_1X2_percentages['X'])
            draw_probability = common_1X2_percentages['X'] - win_extra*common_1X2_percentages['X']/(common_1X2_percentages['1']+common_1X2_percentages['X'])

        if abs(home_rating - away_rating) < close_match_threshold:
            # close match => draw is more probable
            draw_extra = max_draw_extra * (1 - abs(home_rating - away_rating)/close_match_threshold)
            draw_extra = min(draw_extra, 1-draw_probability)
                
            draw_probability += draw_extra
            new_home_win_probability = home_win_probability - draw_extra*(home_win_probability/(home_win_probability+away_win_probability))
            new_away_win_probability = away_win_probability - draw_extra*(away_win_probability/(home_win_probability+away_win_probability))
        
            home_win_probability = new_home_win_probability
            away_win_probability = new_away_win_probability
        
        assert home_win_probability + draw_probability + away_win_probability > 0.99 and home_win_probability + draw_probability + away_win_probability < 1.01 and home_win_probability > 0 and draw_probability > 0 and away_win_probability > 0
        
#        print home_win_probability, draw_probability, away_win_probability
#        print 1/home_win_probability, 1/draw_probability, 1/away_win_probability
        
        # Make bets.

        # Don't make bets until the ELO ratings have been build up.
        if idx > 1000:
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

    '''
    print
    for k,v in reversed(sorted(elo_ratings.items(), key=lambda x: x[1])):
        print k, v
    print

    print 'money left:', money
    print 'number of matches:', len(matches)
    '''
    return money

if __name__ == '__main__':

    POPULATION_SIZE = 100
    MUTATION_PROBABILITY = 0.01

    INITIAL_MONEY = 1000

    LEAGUE = 'SM-LIIGA'
    START = '1900-01-01'

    # Create the initial population.
    population = []
    while len(population) < POPULATION_SIZE:
        population.append({
            'k0': random.randint(0,30) + random.random(),
            'lambda': random.randint(0,2) + random.random(),
            # How big class difference causes the winning probability to raise by one percent.
            'class_difference': random.randint(0,100) + random.random(),
            'close_match_threshold': float(random.randint(0,1000)),
            'max_draw_extra': random.uniform(0.0, 0.5),
            'value': None
        })

    while True:

        # Evaluate the population.
        for obj in population:
#            print obj
            if not obj['value']:
                obj['value'] = main(LEAGUE, START, INITIAL_MONEY, obj['class_difference'], obj['close_match_threshold'], obj['max_draw_extra'], obj['k0'], obj['lambda'])
    
        # Remove the worst half of the population.
        population = list(reversed(sorted(population, key=lambda x: x['value'])))
        population = population[:len(population)/2]
        
        # Get current best.
        best = population[0]          
        mean = sum([x['value'] for x in population])/len(population)
        
        # Generate new objects.
        new_objects = []
        while len(population) + len(new_objects) < POPULATION_SIZE:
            obj = {'value': None}
            
            for key in ['k0', 'lambda', 'class_difference', 'close_match_threshold', 'max_draw_extra']:
                if random.random() <= MUTATION_PROBABILITY:
                    if key == 'k0':
                        obj[key] = random.randint(0,30) + random.random()
                    elif key == 'lambda':
                        obj[key] = random.randint(0,2) + random.random()
                    elif key == 'class_difference':
                        obj[key] = random.randint(0,100) + random.random()
                    elif key == 'close_match_threshold':
                        obj[key] = float(random.randint(0,1000))
                    elif key == 'max_draw_extra':
                        obj[key] = random.uniform(0.0, 0.5)
                    else:
                        raise Exception('unhandled gene: ' + key)
                else:
                    obj[key] = population[random.randint(0, len(population)-1)][key]
            
            new_objects.append(obj)
        population = population + new_objects
            
        # Print current best.
        print 'current best:', best['value'], ':', best
        print 'mean:', mean
