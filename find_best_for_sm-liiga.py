# -*- coding: utf-8 -*-

import db
import estimator as estimator_module
import betting_strategy
import runner
import pickle
import random
import time
import sys

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0
        
def get_random_object():
    obj = {
        # home team home matches
        'home_team_home_match_percentages_history_length_in_matches': random.randint(10, 150),
        'home_team_home_match_percentages_start_weight': random.random(),
        'home_team_home_match_percentages_end_weight': random.uniform(0.5, 1.0),
        'home_team_home_match_weight': random.random(),
    
        # home team matches
        'home_team_match_percentages_history_length_in_matches': random.randint(10, 150),
        'home_team_match_percentages_start_weight': random.random(),
        'home_team_match_percentages_end_weight': random.uniform(0.5, 1.0),
        'home_team_match_weight': random.random(),
        
        # away team away matches
        'away_team_away_match_percentages_history_length_in_matches': random.randint(10, 150),
        'away_team_away_match_percentages_start_weight': random.random(),
        'away_team_away_match_percentages_end_weight': random.uniform(0.5, 1.0),
        'away_team_away_match_weight': random.random(),
        
        # away team matches
        'away_team_match_percentages_history_length_in_matches': random.randint(10, 150),
        'away_team_match_percentages_start_weight': random.random(),
        'away_team_match_percentages_end_weight': random.uniform(0.5, 1.0),
        'away_team_match_weight': random.random(),
        
        # minimum allowed numbers of games
        'minimum_home_team_home_matches_count': random.randint(2, 40),
        'minimum_home_team_matches_count': random.randint(2, 40),
        'minimum_away_team_away_matches_count': random.randint(2, 40),
        'minimum_away_team_matches_count': random.randint(2, 40),
        
        # common 1X2 percentages
        'common_1X2_match_percentages_history_length_in_matches': random.randint(10, 150),
        'common_1X2_match_percentages_start_weight': random.random(),
        'common_1X2_match_percentages_end_weight': random.uniform(0.5, 1.0),
        'common_1X2_match_weight': random.random(),
        
        # over power fix
        'over_power_threshold': random.randint(1,4) + random.random(), # 1.0-5.0
        'over_power_multiplier': random.random(),
        
        # close match fix
        'close_match_threshold': 1 + random.random(),
        'close_match_multiplier': random.random(),
        'close_match_extra': random.randint(0, 30)

    }
    
    if obj['home_team_home_match_percentages_end_weight'] < obj['home_team_home_match_percentages_start_weight']:
        obj['home_team_home_match_percentages_end_weight'] = 1.0
    if obj['home_team_match_percentages_end_weight'] < obj['home_team_match_percentages_start_weight']:
        obj['home_team_match_percentages_end_weight'] = 1.0
    if obj['away_team_away_match_percentages_end_weight'] < obj['away_team_away_match_percentages_start_weight']:
        obj['away_team_away_match_percentages_end_weight'] = 1.0
    if obj['away_team_match_percentages_end_weight'] < obj['away_team_match_percentages_start_weight']:
        obj['away_team_match_percentages_end_weight'] = 1.0
        
    obj['minimum_home_team_home_matches_count'] = min(obj['minimum_home_team_home_matches_count'], obj['home_team_home_match_percentages_history_length_in_matches'])
    obj['minimum_home_team_matches_count'] = min(obj['minimum_home_team_matches_count'], obj['home_team_match_percentages_history_length_in_matches'])
    obj['minimum_away_team_away_matches_count'] = min(obj['minimum_away_team_away_matches_count'], obj['away_team_away_match_percentages_history_length_in_matches'])
    obj['minimum_away_team_matches_count'] = min(obj['minimum_away_team_matches_count'], obj['away_team_match_percentages_history_length_in_matches'])
    
    return obj
        
        
if __name__ == '__main__':
        
    INITIAL_MONEY = 1000
    
    POPULATION_SIZE = 100
    MUTATION_FREQUENCY = 0.05 # 0.0-1.0 probability for new gene to be mutated
    
    BETTING_STRATEGY = betting_strategy.div_100 # betting_strategy.kelly_div_10, betting_strategy.div_10, betting_strategy.div_100, betting_strategy.bet_2, betting_strategy.bet_10

    # Load or create the initial population.
    population = []
    if len(sys.argv) >= 2:
        pickle_file = sys.argv[1]
        with open(pickle_file, 'rb') as f:
            population = pickle.load(f)

        while len(population) < POPULATION_SIZE:
            population.append([get_random_object(), None])

        if sys.argv[2] == 'reset':
            print 'RESETTING...'
            for idx in range(len(population)):
                population[idx][1] = None

    else:
        for idx in range(POPULATION_SIZE):
            population.append([get_random_object(), None])

    population_number = 1
    while True:
        print 'SM-LIIGA POPULATION', population_number
    
        # Evaluate the population.
        for idx, elem in enumerate(population):
        
            print str(idx+1) + '/' + str(POPULATION_SIZE)
        
            if elem[1] is None: # Only calculate value if not previously calculated
                ukko = elem[0]
                print ukko
            
                estimator = estimator_module.get_parameterized_estimator(ukko)
                
                winnings = []
                for season in range(1999, 2016): 
                    print '\tSM-LIIGA ' + str(season) + '-' + str(season+1) + ': ',
                    money_left, matches = runner.play(INITIAL_MONEY, estimator, BETTING_STRATEGY, league=u'SM-LIIGA', season=str(season) + '-' + str(season+1))
                    print money_left
                    
                    if money_left == INITIAL_MONEY:
                        # No bets made
                        winnings.append(-1000)
                    else:
                        winnings.append(money_left - INITIAL_MONEY)
                print 'TOTAL:', sum(winnings)
                
                winnings = list(sorted(winnings))
                print 'winnings:', winnings
                population[idx][0]['winnings'] = winnings
                population[idx][1] = sum(winnings[:len(winnings)/2])
            
            print 'SUM OF WORST HALF:', population[idx][1]


        # Write population to file.
        with open('populations_sm-liiga/' + time.strftime('%Y-%m-%d_%H:%M:%s') + '.pickle', 'wb') as f:
            pickle.dump(population, f)

        # Remove the worst 50 percent.
        population = list(reversed(list(sorted(population, key=lambda x: x[1]))))
        population = population[:len(population)/2]

        # Create offsprings.
        offsprings = []
        while len(population) + len(offsprings) < POPULATION_SIZE:
            parents = [
                population[random.randint(0,len(population)-1)],
                population[random.randint(0,len(population)-1)]
            ]
            
            keys = [
                'home_team_home_match_percentages_history_length_in_matches', 
                'home_team_home_match_percentages_start_weight',
                'home_team_home_match_percentages_end_weight',
                'home_team_home_match_weight',
                'home_team_match_percentages_history_length_in_matches',
                'home_team_match_percentages_start_weight',
                'home_team_match_percentages_end_weight',
                'home_team_match_weight',
                'away_team_away_match_percentages_history_length_in_matches',
                'away_team_away_match_percentages_start_weight',
                'away_team_away_match_percentages_end_weight',
                'away_team_away_match_weight',
                'away_team_match_percentages_history_length_in_matches',
                'away_team_match_percentages_start_weight',
                'away_team_match_percentages_end_weight',
                'away_team_match_weight',
                'minimum_home_team_home_matches_count',
                'minimum_home_team_matches_count',
                'minimum_away_team_away_matches_count',
                'minimum_away_team_matches_count',
                'common_1X2_match_percentages_history_length_in_matches',
                'common_1X2_match_percentages_start_weight',
                'common_1X2_match_percentages_end_weight',
                'common_1X2_match_weight',
                'over_power_threshold',
                'over_power_multiplier',
                'close_match_threshold',
                'close_match_multiplier',
                'close_match_extra'
            ]
            
            mean_pseudo_parent_obj = {}
            for key in keys:
                mean_pseudo_parent_obj[key] = (parents[0][0][key] + parents[1][0][key])/2
            
            mean_pseudo_parent = [
                mean_pseudo_parent_obj, 
                None
            ]
            
            parents.append(mean_pseudo_parent)
            
            offspring_obj = {}
            for key in keys:
                offspring_obj[key] = parents[random.randint(0, 2)][0][key]
            offspring = [
                offspring_obj,
                None
            ]
            
            # Make mutations. Maybe...
            seed_obj = get_random_object()
            for key in keys:
                is_mutate = (random.random() < MUTATION_FREQUENCY)
                if is_mutate:
                    offspring[0][key] = seed_obj[key]

            # Make some rationalizations.
            
            if offspring[0]['home_team_home_match_percentages_end_weight'] < offspring[0]['home_team_home_match_percentages_start_weight']:
                offspring[0]['home_team_home_match_percentages_end_weight'] = 1.0
            if offspring[0]['home_team_match_percentages_end_weight'] < offspring[0]['home_team_match_percentages_start_weight']:
                offspring[0]['home_team_match_percentages_end_weight'] = 1.0
            if offspring[0]['away_team_away_match_percentages_end_weight'] < offspring[0]['away_team_away_match_percentages_start_weight']:
                offspring[0]['away_team_away_match_percentages_end_weight'] = 1.0
            if offspring[0]['away_team_match_percentages_end_weight'] < offspring[0]['away_team_match_percentages_start_weight']:
                offspring[0]['away_team_match_percentages_end_weight'] = 1.0

            offspring[0]['minimum_home_team_home_matches_count'] = min(offspring[0]['minimum_home_team_home_matches_count'], offspring[0]['home_team_home_match_percentages_history_length_in_matches']),
            offspring[0]['minimum_home_team_matches_count'] = min(offspring[0]['minimum_home_team_matches_count'], offspring[0]['home_team_match_percentages_history_length_in_matches']),
            offspring[0]['minimum_away_team_away_matches_count'] = min(offspring[0]['minimum_away_team_away_matches_count'], offspring[0]['away_team_away_match_percentages_history_length_in_matches']),
            offspring[0]['minimum_away_team_matches_count'] = min(offspring[0]['minimum_away_team_matches_count'], offspring[0]['away_team_match_percentages_history_length_in_matches']),
            
            offsprings.append(offspring)

        population = population + offsprings
        
        population_number += 1
