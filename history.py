# -*- coding: utf-8 -*-

import sqlite3

import db


def get_matches(team=None, league=None, season=None, start=None, end=None, cancelled=False, awarded=False):

    if team is not None:
        team_id = db.get_team_id(team)
    else:
        team_id = None

    if league is not None:
        league_id = db.get_league_id(league)
    else:
        league_id = None
        
    if season is not None:
        season_id = db.get_season_id(season)
    else:
        season_id = None
        
    return db.get_matches(team_id=team_id, start=start, end=end, league_id=league_id, season_id=season_id, cancelled=cancelled, awarded=awarded)


def get_n_previous_matches_of_team(team, date, count, league=None, season=None):

    team_id = db.get_team_id(team)

    if league is not None:
        league_id = db.get_league_id(league)
    else:
        league_id = None
        
    if season is not None:
        season_id = db.get_season_id(season)
    else:
        season_id = None
        
    matches = db.get_matches(team_id=team_id, end=date, league_id=league_id, season_id=season_id, cancelled=False, awarded=False)
    
    matches = sorted(matches, key=lambda x: x['date'])
    matches.reverse()
    
    return matches[:min(count, len(matches))]
    

def get_season_table(league, season):
    
    league_id = db.get_league_id(league)
    season_id = db.get_season_id(season)
    
    matches = db.get_matches(league_id=league_id, season_id=season_id, cancelled=False)
    
    teams = {}
    for row in matches:
        home_team = row['home_team']
        away_team = row['away_team']
        full_time_home_team_goals = row['full_time_home_team_goals']
        full_time_away_team_goals = row['full_time_away_team_goals']
        extra_time_home_team_goals = row['extra_time_home_team_goals']
        extra_time_away_team_goals = row['extra_time_away_team_goals']
        penalties_home_team_goals = row['penalties_home_team_goals']
        penalties_away_team_goals = row['penalties_away_team_goals']
        
        if home_team not in teams:
            teams[home_team] = 0
        if away_team not in teams:
            teams[away_team] = 0
        
        # full time home win
        if full_time_home_team_goals > full_time_away_team_goals:
            teams[home_team] += 3
        # full time away win
        elif full_time_home_team_goals < full_time_away_team_goals:
            teams[away_team] += 3
        # extra time home win
        elif extra_time_home_team_goals > extra_time_away_team_goals:
            teams[home_team] += 2
            teams[away_team] += 1
        # extra time away win
        elif extra_time_home_team_goals < extra_time_away_team_goals:
            teams[home_team] += 1
            teams[away_team] += 2
        # penalties home win
        elif penalties_home_team_goals > penalties_away_team_goals:
            teams[home_team] += 2
            teams[away_team] += 1
        # penalties away win
        elif penalties_home_team_goals < penalties_away_team_goals:
            teams[home_team] += 1
            teams[away_team] += 2
        else:
            raise Exception('unhandled case')
            
    result = teams.items()
    return reversed(sorted(result, key=lambda x: x[1]))


def get_full_time_match_percentages_of_team(team, league=None, season=None, start=None, end=None):
    '''returns win%, draw%, loss%'''

    team_id = db.get_team_id(team)
    
    if league:
        league_id = db.get_league_id(league)
    else:
        league_id = None

    if season:
        season_id = db.get_season_id(season)
    else:
        season_id = None

    matches = db.get_matches(team_id=team_id, season_id=season_id, league_id=league_id, start=start, end=end, cancelled=False, awarded=False)
    
    num_of_games = len(matches)
    wins = 0
    draws = 0
    losses = 0
    for row in matches:
        home_team_id = row['home_team_id']
        away_team_id = row['away_team_id']
        full_time_home_team_goals = row['full_time_home_team_goals']
        full_time_away_team_goals = row['full_time_away_team_goals']
        
        if home_team_id == team_id:
            if full_time_home_team_goals > full_time_away_team_goals:
                wins += 1
            elif full_time_home_team_goals < full_time_away_team_goals:
                losses += 1
            else:
                draws += 1
        elif away_team_id == team_id:
            if full_time_home_team_goals < full_time_away_team_goals:
                wins += 1
            elif full_time_home_team_goals > full_time_away_team_goals:
                losses += 1
            else:
                draws += 1
        else:
            raise Exeption('not a game of the team ' + team)

    if num_of_games == 0:
        return (0,0,0,0)
    else:
        return (float(wins)/num_of_games,
                float(draws)/num_of_games,
                float(losses)/num_of_games,
                num_of_games)


def get_full_time_home_match_percentages_of_team(team, league=None, season=None, start=None, end=None):
    '''returns win%, draw%, loss%'''

    team_id = db.get_team_id(team)
    
    if league:
        league_id = db.get_league_id(league)
    else:
        league_id = None

    if season:
        season_id = db.get_season_id(season)
    else:
        season_id = None

    matches = db.get_matches(home_team_id=team_id, season_id=season_id, league_id=league_id, start=start, end=end, cancelled=False, awarded=False)
   
    num_of_games = len(matches)
    wins = 0
    draws = 0
    losses = 0
    for g in matches:
        if g['full_time_home_team_goals'] > g['full_time_away_team_goals']:
            wins += 1
        elif g['full_time_home_team_goals'] < g['full_time_away_team_goals']:
            losses += 1
        else:
            draws += 1
            
    if num_of_games == 0:
        return (0,0,0,0)
    else:
        return (float(wins)/num_of_games,
                float(draws)/num_of_games,
                float(losses)/num_of_games,
                num_of_games)
    
    
def get_full_time_away_match_percentages_of_team(team, league=None, season=None, start=None, end=None):
    '''returns win%, draw%, loss%'''

    team_id = db.get_team_id(team)
    
    if league:
        league_id = db.get_league_id(league)
    else:
        league_id = None

    if season:
        season_id = db.get_season_id(season)
    else:
        season_id = None

    matches = db.get_matches(away_team_id=team_id, season_id=season_id, league_id=league_id, start=start, end=end, cancelled=False, awarded=False)
   
    num_of_games = len(matches)
    wins = 0
    draws = 0
    losses = 0
    for g in matches:
        if g['full_time_home_team_goals'] < g['full_time_away_team_goals']:
            wins += 1
        elif g['full_time_home_team_goals'] > g['full_time_away_team_goals']:
            losses += 1
        else:
            draws += 1
            
    if num_of_games == 0:
        return (0,0,0,0)
    else:
        return (float(wins)/num_of_games,
                float(draws)/num_of_games,
                float(losses)/num_of_games,
                num_of_games)
    

def get_full_time_1X2_percentages(league=None, season=None, start=None, end=None):

    if league:
        league_id = db.get_league_id(league)
    else:
        league_id = None

    if season:
        season_id = db.get_season_id(season)
    else:
        season_id = None

    matches = db.get_matches(season_id=season_id, league_id=league_id, start=start, end=end, cancelled=False, awarded=False)
    
    num_of_matches = len(matches)
    home_win = 0
    draw = 0
    away_win = 0
    
    for match in matches:
        if match['full_time_home_team_goals'] > match['full_time_away_team_goals']:
            home_win += 1
        elif match['full_time_home_team_goals'] < match['full_time_away_team_goals']:
            away_win += 1
        else:
            draw += 1
            
    if num_of_matches == 0:
        return (0,0,0,0)
    else:
        return (float(home_win)/num_of_matches,
                float(draw)/num_of_matches,
                float(away_win)/num_of_matches,
                num_of_matches)

