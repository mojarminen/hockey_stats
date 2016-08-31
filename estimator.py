# -*- coding: utf-8 -*-

import datetime
import math

import history
import db

def simple_estimation(home_team, away_team, date, season=None, league=None):

    HISTORY_IN_WEEKS = 26
    COMMON_HISTORY_WEIGHT = 0.01

    year, month, day = [int(d) for d in date.split('-')]
    start = datetime.date(year, month, day) + datetime.timedelta(weeks=-HISTORY_IN_WEEKS)
    start = start.strftime('%Y-%m-%d')
    
    
#    h1, hX, h2, h_count = history.get_home_match_percentages_of_team(home_team, league=league, season=season, start=start, end=date)
#    a2, aX, a1, a_count = history.get_away_match_percentages_of_team(away_team, league=league, season=season, start=start, end=date)
    h1, hX, h2, h_count = history.get_full_time_home_match_percentages_of_team(home_team, league=league, season=None, start=start, end=date)
    a2, aX, a1, a_count = history.get_full_time_away_match_percentages_of_team(away_team, league=league, season=None, start=start, end=date)
    c1, cX, c2, c_count = history.get_full_time_1X2_percentages(league=league, start=start, end=date)

    if h_count < 5 or a_count < 5:
        return None

    result = {'1': h1*(float(h_count)/(h_count+a_count)) + a1*(float(a_count)/(h_count+a_count)),
              'X': hX*(float(h_count)/(h_count+a_count)) + aX*(float(a_count)/(h_count+a_count)),
              '2': h2*(float(h_count)/(h_count+a_count)) + a2*(float(a_count)/(h_count+a_count)), 
              'home_team_games': h_count, 
              'away_team_games': a_count}
              
    result['1'] = result['1'] * (1 - COMMON_HISTORY_WEIGHT) + c1 * COMMON_HISTORY_WEIGHT
    result['X'] = result['X'] * (1 - COMMON_HISTORY_WEIGHT) + cX * COMMON_HISTORY_WEIGHT
    result['2'] = result['2'] * (1 - COMMON_HISTORY_WEIGHT) + c2 * COMMON_HISTORY_WEIGHT
    
    return result


def simple_estimation2(home_team, away_team, date, season=None, league=None):
    
    NUMBER_OF_LONG_TIME_MATCHES = 30
    NUMBER_OF_SHORT_TIME_MATCHES = 5
    
    # Get home team's long time home game percentages.    
    # Get home team's long time game percentages.
    matches = history.get_n_previous_matches_of_team(home_team, date, NUMBER_OF_LONG_TIME_MATCHES, league=league, season=None)
    if len(matches) < NUMBER_OF_LONG_TIME_MATCHES:
        return None

    wins = 0
    draws = 0
    losses = 0

    home_wins = 0
    home_draws = 0
    home_losses = 0

    home_games = 0

    for m in matches:
        if m['home_team'] == home_team:
            home_games += 1
            if m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                wins += 1
                home_wins += 1
            elif m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                losses += 1
                home_losses += 1
            else:
                draws += 1
                home_draws += 1
        elif m['away_team'] == home_team:
            if m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        else:
            raise Exception('invalid game')

    home_team_long_time_win_percentage = float(wins)/len(matches)
    home_team_long_time_draw_percentage = float(draws)/len(matches)
    home_team_long_time_loss_percentage = float(losses)/len(matches)

    home_team_long_time_home_win_percentage = float(home_wins)/home_games
    home_team_long_time_home_draw_percentage = float(home_draws)/home_games
    home_team_long_time_home_loss_percentage = float(home_losses)/home_games
    
    # Get away team's long time away game percentages.    
    # Get away team's long time game percentages. 

    matches = history.get_n_previous_matches_of_team(away_team, date, NUMBER_OF_LONG_TIME_MATCHES, league=league, season=None)
    if len(matches) < NUMBER_OF_LONG_TIME_MATCHES:
        return None

    wins = 0
    draws = 0
    losses = 0

    away_wins = 0
    away_draws = 0
    away_losses = 0

    away_games = 0

    for m in matches:
        if m['home_team'] == away_team:
            if m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        elif m['away_team'] == away_team:
            away_games += 1
            if m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                wins += 1
                away_wins += 1
            elif m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                losses += 1
                away_losses += 1
            else:
                draws += 1
                away_draws += 1
        else:
            raise Exception('invalid game')
            
    away_team_long_time_win_percentage = float(wins)/len(matches)
    away_team_long_time_draw_percentage = float(draws)/len(matches)
    away_team_long_time_loss_percentage = float(losses)/len(matches)
    
    away_team_long_time_away_win_percentage = float(away_wins)/away_games
    away_team_long_time_away_draw_percentage = float(away_draws)/away_games
    away_team_long_time_away_loss_percentage = float(away_losses)/away_games
    
    # Get home team's short time game percentages.
    matches = history.get_n_previous_matches_of_team(home_team, date, NUMBER_OF_SHORT_TIME_MATCHES, league=league, season=None)
    if len(matches) < NUMBER_OF_SHORT_TIME_MATCHES:
        return None
    wins = 0
    draws = 0
    losses = 0
    for m in matches:
        if m['home_team'] == home_team:
            if m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        elif m['away_team'] == home_team:
            if m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        else:
            raise Exception('invalid game')
    home_team_short_time_win_percentage = float(wins)/len(matches)
    home_team_short_time_draw_percentage = float(draws)/len(matches)
    home_team_short_time_loss_percentage = float(losses)/len(matches)
    
    # Get away team's short time game percentages. 
    matches = history.get_n_previous_matches_of_team(away_team, date, NUMBER_OF_SHORT_TIME_MATCHES, league=league, season=None)
    if len(matches) < NUMBER_OF_SHORT_TIME_MATCHES:
        return None
    wins = 0
    draws = 0
    losses = 0
    for m in matches:
        if m['home_team'] == away_team:
            if m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        elif m['away_team'] == away_team:
            if m['full_time_home_team_goals'] < m['full_time_away_team_goals']:
                wins += 1
            elif m['full_time_home_team_goals'] > m['full_time_away_team_goals']:
                losses += 1
            else:
                draws += 1
        else:
            raise Exception('invalid game')
    away_team_short_time_win_percentage = float(wins)/len(matches)
    away_team_short_time_draw_percentage = float(draws)/len(matches)
    away_team_short_time_loss_percentage = float(losses)/len(matches)
    
    
    long_time_percentages = (home_team_long_time_win_percentage*0.5 + away_team_long_time_loss_percentage*0.5,
                             home_team_long_time_draw_percentage*0.5 + away_team_long_time_draw_percentage*0.5,
                             home_team_long_time_loss_percentage*0.5 + away_team_long_time_win_percentage*0.5)
    
    short_time_percentages = (home_team_short_time_win_percentage*0.5 + away_team_short_time_loss_percentage*0.5,
                              home_team_short_time_draw_percentage*0.5 + away_team_short_time_draw_percentage*0.5,
                              home_team_short_time_loss_percentage*0.5 + away_team_short_time_win_percentage*0.5)
                              
    home_advantage = (home_team_long_time_home_win_percentage*0.5 + away_team_long_time_away_loss_percentage*0.5,
                      home_team_long_time_home_draw_percentage*0.5 + away_team_long_time_away_draw_percentage*0.5,
                      home_team_long_time_home_loss_percentage*0.5 + away_team_long_time_away_win_percentage*0.5)

    result = {'1': long_time_percentages[0]*0.4 + short_time_percentages[0]*0.2 + home_advantage[0]*0.4, 
              'X': long_time_percentages[1]*0.4 + short_time_percentages[1]*0.2 + home_advantage[1]*0.4, 
              '2': long_time_percentages[2]*0.4 + short_time_percentages[2]*0.2 + home_advantage[2]*0.4}
    
    return result
    
    
def poisson(home_team, away_team, date, season=None, league=None):
    HISTORY_IN_WEEKS = 52
    
    year, month, day = [int(d) for d in date.split('-')]
    start = datetime.date(year, month, day) + datetime.timedelta(weeks=-HISTORY_IN_WEEKS)
    start = start.strftime('%Y-%m-%d')
    matches = history.get_matches(league=league, start=start, end=date)
    if len(matches) == 0:
        return None

    # Get the mean values of home goals and away goals per game.
    home_goals = 0
    away_goals = 0
    for m in matches:
        home_goals += m['full_time_home_team_goals']
        away_goals += m['full_time_away_team_goals']
    average_goals_scored_at_home = float(home_goals)/len(matches)
    average_goals_scored_away = float(away_goals)/len(matches)
    average_goals_conceded_at_home = average_goals_scored_away
    average_goals_conceded_away = average_goals_scored_at_home
    
    # Estimate home team goals.
    
    # Calculate home team attack strength.
    home_goals = 0
    number_of_matches = 0
    for m in matches:
        if m['home_team'] == home_team:
            home_goals += m['full_time_home_team_goals']
            number_of_matches += 1
    if number_of_matches == 0:
        return None
    home_attack_strength = (float(home_goals)/number_of_matches)/average_goals_scored_at_home
    
    # Calculate away team defence strength.
    home_goals = 0
    number_of_matches = 0
    for m in matches:
        if m['away_team'] == away_team:
            home_goals += m['full_time_home_team_goals']
            number_of_matches += 1
    if number_of_matches == 0:
        return None
    away_defence_strength = (float(home_goals)/number_of_matches)/average_goals_conceded_away
    
    home_goals_estimation = home_attack_strength * away_defence_strength * average_goals_scored_at_home
    
    # Calculate away team attack strength.
    
    # Estimate away_team goals.
    away_goals = 0
    number_of_matches = 0
    for m in matches:
        if m['away_team'] == away_team:
            away_goals += m['full_time_away_team_goals']
            number_of_matches += 1
    if number_of_matches == 0:
        return None
    away_attack_strength = (float(away_goals)/number_of_matches)/average_goals_scored_away
    
    # Calculate home team defence strength.
    away_goals = 0
    number_of_matches = 0
    for m in matches:
        if m['home_team'] == home_team:
            away_goals += m['full_time_away_team_goals']
            number_of_matches += 1
    if number_of_matches == 0:
        return None
    home_defence_strength = (float(away_goals)/number_of_matches)/average_goals_conceded_at_home
    
    away_goals_estimation = away_attack_strength * home_defence_strength * average_goals_scored_away
    
    home_win_probability = 0
    draw_probability = 0
    away_win_probability = 0
    for h in range(0,10):
        for a in range(0,10):
            h_probability = (math.pow(math.e, -home_goals_estimation) * math.pow(home_goals_estimation, h))/math.factorial(h)
            a_probability = (math.pow(math.e, -away_goals_estimation) * math.pow(away_goals_estimation, a))/math.factorial(a)
            probability = h_probability * a_probability 
            if h > a:
                home_win_probability += probability
            elif h < a:
                away_win_probability += probability
            else:
                draw_probability += probability
    
    assert home_win_probability + draw_probability + away_win_probability <= 1
    
    if home_win_probability < 0.05 or draw_probability < 0.05 or away_win_probability < 0.05:
        return None

    result = {'1': home_win_probability,
              'X': draw_probability,
              '2': away_win_probability}

    return result


def get_parameterized_estimator(params):
    
    # home team home matches
    home_team_home_match_percentages_history_length_in_matches = params['home_team_home_match_percentages_history_length_in_matches']
    home_team_home_match_percentages_start_weight = params['home_team_home_match_percentages_start_weight']
    home_team_home_match_percentages_end_weight = params['home_team_home_match_percentages_end_weight']
    home_team_home_match_weight = params['home_team_home_match_weight']
    
    # home team matches
    home_team_match_percentages_history_length_in_matches = params['home_team_match_percentages_history_length_in_matches']
    home_team_match_percentages_start_weight = params['home_team_match_percentages_start_weight']
    home_team_match_percentages_end_weight = params['home_team_match_percentages_end_weight']
    home_team_match_weight = params['home_team_match_weight']
    
    # away team away matches
    away_team_away_match_percentages_history_length_in_matches = params['away_team_away_match_percentages_history_length_in_matches']
    away_team_away_match_percentages_start_weight = params['away_team_away_match_percentages_start_weight']
    away_team_away_match_percentages_end_weight = params['away_team_away_match_percentages_end_weight']
    away_team_away_match_weight = params['away_team_away_match_weight']
    
    # away team matches
    away_team_match_percentages_history_length_in_matches = params['away_team_match_percentages_history_length_in_matches']
    away_team_match_percentages_start_weight = params['away_team_match_percentages_start_weight']
    away_team_match_percentages_end_weight = params['away_team_match_percentages_end_weight']
    away_team_match_weight = params['away_team_match_weight']
    
    # minimum allowed numbers of games
    minimum_home_team_home_matches_count = params['minimum_home_team_home_matches_count']
    minimum_home_team_matches_count = params['minimum_home_team_matches_count']
    minimum_away_team_away_matches_count = params['minimum_away_team_away_matches_count']
    minimum_away_team_matches_count = params['minimum_away_team_matches_count']
    
    # common 1X2 percentages
    common_1X2_match_percentages_history_length_in_matches = params['common_1X2_match_percentages_history_length_in_matches']
    common_1X2_match_percentages_start_weight = params['common_1X2_match_percentages_start_weight']
    common_1X2_match_percentages_end_weight = params['common_1X2_match_percentages_end_weight']
    common_1X2_match_weight = params['common_1X2_match_weight']
    
    # over power fix
    over_power_threshold = params['over_power_threshold']
    over_power_multiplier = params['over_power_multiplier']
    
    # close match fix
    close_match_threshold = params['close_match_threshold']
    close_match_multiplier = params['close_match_multiplier']
    close_match_extra = params['close_match_extra']
    
    # strain fix (how many games before the game)
    # TODO
    
    def parameterized_estimator(home_team, away_team, date, season=None, league=None):
        
        h_h1, h_hX, h_h2, h_h_count = history.get_full_time_home_match_percentages_of_team(home_team, 
                                                                                           league=league, 
                                                                                           end=date, 
                                                                                           start_weight=home_team_home_match_percentages_start_weight, 
                                                                                           end_weight=home_team_home_match_percentages_end_weight,
                                                                                           number_of_matches=home_team_home_match_percentages_history_length_in_matches)
                                                                                           
        h_m1, h_mX, h_m2, h_m_count = history.get_full_time_match_percentages_of_team(home_team, 
                                                                                      league=league, 
                                                                                      end=date, 
                                                                                      start_weight=home_team_match_percentages_start_weight, 
                                                                                      end_weight=home_team_match_percentages_end_weight,
                                                                                      number_of_matches=home_team_match_percentages_history_length_in_matches)
        
        a_a2, a_aX, a_a1, a_a_count = history.get_full_time_away_match_percentages_of_team(away_team, 
                                                                                           league=league, 
                                                                                           end=date, 
                                                                                           start_weight=away_team_away_match_percentages_start_weight, 
                                                                                           end_weight=away_team_away_match_percentages_end_weight,
                                                                                           number_of_matches=away_team_away_match_percentages_history_length_in_matches)
                                                                                           
        a_m2, a_mX, a_m1, a_m_count = history.get_full_time_match_percentages_of_team(away_team, 
                                                                                      league=league, 
                                                                                      end=date, 
                                                                                      start_weight=away_team_match_percentages_start_weight, 
                                                                                      end_weight=away_team_match_percentages_end_weight,
                                                                                      number_of_matches=away_team_match_percentages_history_length_in_matches)
        
        c1, cX, c2, c_count = history.get_full_time_1X2_percentages(league=league, 
                                                                    end=date,
                                                                    start_weight=common_1X2_match_percentages_start_weight,
                                                                    end_weight=common_1X2_match_percentages_end_weight,
                                                                    number_of_matches=common_1X2_match_percentages_history_length_in_matches)

        if (h_h_count < minimum_home_team_home_matches_count 
                or a_a_count < minimum_away_team_away_matches_count 
                or h_m_count < minimum_home_team_matches_count 
                or a_m_count < minimum_away_team_matches_count):
            return None

        result = {}

        result['1'] = float(
                        h_h1*home_team_home_match_weight + 
                        h_m1*home_team_match_weight + 
                        a_a1*away_team_away_match_weight + 
                        a_m1*away_team_match_weight + 
                        c1*common_1X2_match_weight
                      )/(home_team_home_match_weight + home_team_match_weight + away_team_away_match_weight + away_team_match_weight + common_1X2_match_weight)
        result['X'] = float(
                        h_hX*home_team_home_match_weight + 
                        h_mX*home_team_match_weight + 
                        a_aX*away_team_away_match_weight + 
                        a_mX*away_team_match_weight + 
                        cX*common_1X2_match_weight
                      )/(home_team_home_match_weight + home_team_match_weight + away_team_away_match_weight + away_team_match_weight + common_1X2_match_weight)
        result['2'] = float(
                        h_h2*home_team_home_match_weight + 
                        h_m2*home_team_match_weight + 
                        a_a2*away_team_away_match_weight + 
                        a_m2*away_team_match_weight + 
                        c2*common_1X2_match_weight
                      )/(home_team_home_match_weight + home_team_match_weight + away_team_away_match_weight + away_team_match_weight + common_1X2_match_weight)
        
        # Fix probabilities based on the nature of the game.
        
        # Over power
        if result['1']/result['2'] > over_power_threshold:
            extra = (result['1']/result['2'])* over_power_multiplier
            result['1'] += extra
            result['2'] -= extra
        elif result['2']/result['1'] > over_power_threshold:
            extra = (result['2']/result['1'])* over_power_multiplier
            result['2'] += extra
            result['1'] -= extra

        # Close match
        if result['1']/result['2'] < (close_match_threshold) and result['2']/result['1'] < (close_match_threshold): # close_match_threshold should be a little over 1
            if result['1'] > result['2']:
                extra = (result['2']/result['1']) * close_match_multiplier * close_match_extra
            else:
                extra = (result['1']/result['2']) * close_match_multiplier * close_match_extra
                
            result['1'] -= extra/2.
            result['2'] -= extra/2.
            result['X'] += extra
        
        return result
    
    return parameterized_estimator
    

'''
HISTORY_IN_WEEKS = 104
START_WEIGHT = 0.5
END_WEIGHT = 1.0
OVER_POWER_THRESHOLD = 1.5
OVER_POWER_EXTRA = 0.07
CLOSE_MATCH_THRESHOLD = 0.1
CLOSE_MATCH_TRIM = 0.02
'''
HISTORY_IN_WEEKS = 109
#HISTORY_IN_MATCHES = 30
HISTORY_IN_MATCHES = None
START_WEIGHT = 0.26845183747363105
END_WEIGHT = 0.5087660101221416
OVER_POWER_THRESHOLD = 1.61868158875048
OVER_POWER_EXTRA = 0.1154001710943926
CLOSE_MATCH_THRESHOLD = 0.22632442451841667
CLOSE_MATCH_TRIM = 0.04303122029883997

def direct(home_team, away_team, date, season=None, league=None):
    
    global HISTORY_IN_WEEKS, START_WEIGHT, END_WEIGHT, OVER_POWER_THRESHOLD, OVER_POWER_EXTRA, CLOSE_MATCH_THRESHOLD, CLOSE_MATCH_TRIM, HISTORY_IN_MATCHES
    
    if HISTORY_IN_WEEKS:
        year, month, day = [int(d) for d in date.split('-')]
        start = datetime.date(year, month, day) + datetime.timedelta(weeks=-HISTORY_IN_WEEKS)
        start = start.strftime('%Y-%m-%d')
    else:
        start = None

    if HISTORY_IN_MATCHES:
        half_of_matches = HISTORY_IN_MATCHES/2
    else:
        half_of_matches = None
        
    h_h1, h_hX, h_h2, h_h_count = history.get_full_time_home_match_percentages_of_team(home_team, league=league, season=None, start=start, 
                                                                                       end=date, start_weight=START_WEIGHT, end_weight=END_WEIGHT,
                                                                                       number_of_matches=half_of_matches)
    h_m1, h_mX, h_m2, h_m_count = history.get_full_time_match_percentages_of_team(home_team, league=league, season=None, start=start, 
                                                                                  end=date, start_weight=START_WEIGHT, end_weight=END_WEIGHT,
                                                                                  number_of_matches=HISTORY_IN_MATCHES)
    
    a_a2, a_aX, a_a1, a_a_count = history.get_full_time_away_match_percentages_of_team(away_team, league=league, season=None, start=start, 
                                                                                       end=date, start_weight=START_WEIGHT, end_weight=END_WEIGHT,
                                                                                       number_of_matches=half_of_matches)
    a_m2, a_mX, a_m1, a_m_count = history.get_full_time_match_percentages_of_team(away_team, league=league, season=None, start=start, 
                                                                                  end=date, start_weight=START_WEIGHT, end_weight=END_WEIGHT,
                                                                                  number_of_matches=HISTORY_IN_MATCHES)
    
    c1, cX, c2, c_count = history.get_full_time_1X2_percentages(league=league, start=start, end=date)

    if h_h_count < 5 or a_a_count < 5 or h_m_count < 10 or a_m_count < 10:
        return None

    result = {}

    result['1'] = float(h_h1 + h_m1 + a_a1 + a_m1 + c1)/5
    result['X'] = float(h_hX + h_mX + a_aX + a_mX + cX)/5
    result['2'] = float(h_h2 + h_m2 + a_a2 + a_m2 + c2)/5
    
    # Fix probabilities based on the nature of the game.
    if result['1']/result['2'] > OVER_POWER_THRESHOLD:
        result['1'] += OVER_POWER_EXTRA
        result['2'] -= OVER_POWER_EXTRA
    elif result['2']/result['1'] > OVER_POWER_THRESHOLD:
        result['2'] += OVER_POWER_EXTRA
        result['1'] -= OVER_POWER_EXTRA

    if result['1']/result['2'] > (1-CLOSE_MATCH_THRESHOLD) and result['1']/result['2'] < (1+CLOSE_MATCH_THRESHOLD):
        result['1'] -= CLOSE_MATCH_TRIM/2.
        result['2'] -= CLOSE_MATCH_TRIM/2.
        result['X'] += CLOSE_MATCH_TRIM
    
    return result



if __name__ == '__main__':
#    print db.get_teams()
    
#    print simple_estimation('Tampereen Ilves', 'HIFK Fotboll', start='2016-01-01', end='2016-08-13', season='2016', league='Veikkausliiga')
#    print simple_estimation('Tampereen Ilves', 'HIFK Fotboll', start='2015-01-01', end='2016-08-13', league='Veikkausliiga')

    poisson('Tampereen Ilves', 'HIFK Fotboll', '2016-08-13', league='Veikkausliiga')
    
