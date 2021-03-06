# -*- coding: utf-8 -*-

import sqlite3
from StringIO import StringIO

DB_FILE = 'hockey.db'
conn = sqlite3.connect(DB_FILE)

tempfile = StringIO()
for line in conn.iterdump():
    tempfile.write('%s\n' % line)
conn.close()
tempfile.seek(0)

# Create a database in memory and import from tempfile
conn = sqlite3.connect(":memory:")
conn.cursor().executescript(tempfile.read())
conn.commit()
conn.row_factory = sqlite3.Row
    
    
def get_match_1X2_odds(match_id):
    cur = conn.cursor()
    
    cur.execute('''SELECT booker, home_win, draw, away_win FROM odds_1X2 WHERE match = ?''', (match_id,))
    
    result = {}
    for row in cur.fetchall():
        booker = row[0]
        home_win = row[1]
        draw = row[2]
        away_win = row[3]
        
        result[booker] = {'home_win': home_win, 'draw': draw, 'away_win': away_win}
    
    return result
    
def get_matches(team_id=None, home_team_id=None, away_team_id=None, 
                league_id=None, season_id=None, # conference_id=None, division_id=None, 
                start=None, end=None, cancelled=None, awarded=None):
    
    if team_id is not None and type(team_id) is not int:
        raise Exception('Invalid type for team_id %s' % str(type(team_id)))
    if home_team_id is not None and type(home_team_id) is not int:
        raise Exception('Invalid type for home_team_id %s' % str(type(home_team_id)))
    if away_team_id is not None and type(away_team_id) is not int:
        raise Exception('Invalid type for away_team_id %s' % str(type(away_team_id)))
    if league_id is not None and type(league_id) is not int:
        raise Exception('Invalid type for league_id %s' % str(type(league_id)))
    if season_id is not None and type(season_id) is not int:
        raise Exception('Invalid type for season_id %s' % str(type(season_id)))
#    if conference_id is not None and type(conference_id) is not int:
#        raise Exception('Invalid type for conference_id %s' % str(type(conference_id)))
#    if division_id is not None and type(division_id) is not int:
#        raise Exception('Invalid type for division_id %s' % str(type(division_id)))
    if start is not None:
        year, month, day = [int(s) for s in start.split('-')]
        assert year >= 1900 and year <= 2100
        assert month >= 1 and month <= 12
        assert day >= 1 and day <= 31
    if end is not None:
        year, month, day = [int(s) for s in end.split('-')]
        assert year >= 1900 and year <= 2100
        assert month >= 1 and month <= 12
        assert day >= 1 and day <= 31
    if cancelled is not None and type(cancelled) is not bool:
        raise Exception('Invalid type for cancelled %s' % str(type(cancelled)))
    if awarded is not None and type(awarded) is not bool:
        raise Exception('Invalid type for awarded %s' % str(type(awarded)))

    cur = conn.cursor()

    query = '''SELECT home_team.id, away_team.id, match.date, match.full_time_home_team_goals, 
               match.full_time_away_team_goals, match.cancelled, match.awarded, home_team.title, away_team.title, 
               league.id, league.title, season.id, season.title, match.id, match.extra_time_home_team_goals, 
               match.extra_time_away_team_goals, match.penalties_home_team_goals, match.penalties_away_team_goals
               FROM match, team as home_team, team as away_team, competition, league, season
               WHERE match.home_team = home_team.id
               AND match.away_team = away_team.id
               AND match.competition = competition.id
               AND competition.league = league.id
               AND competition.season = season.id '''

    if league_id is not None:
        query += ' AND league.id = %s ' % league_id
    if season_id is not None:
        query += ' AND season.id = %s ' % season_id
#    if conference_id is not None:
#        query += ' AND conference.id = %s ' % conference_id
#    if division_id is not None:
#        query += ' AND division.id = %s ' % division_id
    if team_id is not None:
        query += ' AND (home_team.id = %s OR away_team.id = %s)' % (team_id, team_id)
    if home_team_id is not None:
        query += ' AND home_team.id = %s' % home_team_id
    if away_team_id is not None:
        query += ' AND away_team.id = %s' % away_team_id
    if start is not None:
        query += " AND match.date >= '%s' " % start
    if end is not None:
        query += " AND match.date < '%s' " % end
    if cancelled is not None:
        if cancelled:
            query += " AND match.cancelled = 1 "
        else:
            query += " AND match.cancelled = 0 "
    if awarded is not None:
        if awarded:
            query += " AND match.awarded = 1 "
        else:
            query += " AND match.awarded = 0 "
            
    query += " ORDER BY date "
    cur.execute(query)
    
    matches = []
    for row in cur.fetchall():
        matches.append({'home_team_id': row[0],
                        'away_team_id': row[1],
                        'date': row[2],
                        'full_time_home_team_goals': row[3],
                        'full_time_away_team_goals': row[4],
                        'cancelled': bool(row[5]),
                        'awarded': bool(row[6]),
                        'home_team': row[7],
                        'away_team': row[8],
                        'league_id': row[9],
                        'league': row[10],
                        'season_id': row[11],
                        'season': row[12],
                        'match_id': row[13],
                        'extra_time_home_team_goals': row[14], 
                        'extra_time_away_team_goals': row[15], 
                        'penalties_home_team_goals': row[16], 
                        'penalties_away_team_goals': row[17],                       
                       })

    return matches



LEAGUE_IDS = {}
def get_league_id(league):
    global LEAGUE_IDS
    
    if league in LEAGUE_IDS:
        return LEAGUE_IDS[league]
    
    cur = conn.cursor()
    cur.execute('''SELECT id FROM league WHERE title = ?''', (league,))
    result = cur.fetchone()
    if not result:
        raise Exception("No league found '%s'" % team)
        
    LEAGUE_IDS[league] = result[0]
    return result[0]
    

SEASON_IDS = {}
def get_season_id(season):
    global SEASON_IDS
    
    if season in SEASON_IDS:
        return SEASON_IDS[season]
    
    cur = conn.cursor()
    cur.execute('''SELECT id FROM season WHERE title = ?''', (season,))
    result = cur.fetchone()
    if not result:
        raise Exception("No season found '%s'" % season)
    
    SEASON_IDS[season] = result[0]
    return result[0]
    

TEAM_IDS = {}
def get_team_id(team):
    global TEAM_IDS
    
    if team in TEAM_IDS:
        return TEAM_IDS[team]
    
    cur = conn.cursor()
    cur.execute('''SELECT id FROM team WHERE title = ?''', (team,))
    result = cur.fetchone()
    if not result:
        raise Exception("No team found '%s'" % team)
    
    TEAM_IDS[team] = result[0]
    return result[0]


def get_team_name(team_id):
    cur = conn.cursor()
    cur.execute('''SELECT title FROM team WHERE id = ?''', (team_id,))
    result = cur.fetchone()
    if not result:
        raise Exception("No team found with id %s" % team)
    return result[0]


def get_teams():
    cur = conn.cursor()
    cur.execute('''SELECT id, title FROM team''')
    return cur.fetchall()

