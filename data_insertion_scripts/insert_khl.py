# -*- coding: utf-8 -*-

import os
import os.path
import csv
import datetime
import sqlite3

DATA_PATH = '../datafiles/khl'

DB_FILE = '../hockey.db'
conn = sqlite3.connect(DB_FILE)

TEAMS = {
    'KHL': {
        '2008-2009': {
            'Western Conference': {
                'Bobrov': {
                    'Salavat Yulaev Ufa': None,
                    'Atlant Moscow Oblast': None,
                    'Spartak Moscow': None,
                    'Severstal Cherepovets': None,
                    'Metallurg Novokuznetsk': None,
                    'Dinamo Minsk': None,
                },
                'Tarasov': {
                    'CSKA Moscow': None,
                    'Metallurg Magnitogorsk': None,
                    'SKA Saint Petersburg': None,
                    'Traktor Chelyabinsk': None,
                    'HC MVD': None,
                    'Khimik Voskresensk': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Lokomotiv Yaroslavl': None,
                    'Dinamo Riga': None,
                    'Lada Togliatti': None,
                    'Avangard Omsk': None,
                    'Sibir Novosibirsk': None,
                    'Amur Khabarovsk': None,
                },
                'Chernyshev': {
                    'Ak Bars Kazan': None,
                    'Dynamo Moscow': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Barys Astana': None,
                    'Vityaz Chekhov': None, # HC Vityaz
                }
            }
        },
        '2009-2010': {
            'Western Conference': {
                'Bobrov': {
                    'SKA Saint Petersburg': None,
                    'Dynamo Moscow': None,
                    'HC Spartak Moscow': None,
                    'CSKA Moscow': None,
                    'Dinamo Riga': None,
                    'Dinamo Minsk': None,
                },
                'Tarasov': {
                    'HC MVD': None,
                    'Atlant Moscow Oblast': None,
                    'Lokomotiv Yaroslavl': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Severstal Cherepovets': None,
                    'Vityaz Chekhov': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Metallurg Magnitogorsk': None,
                    'Ak Bars Kazan': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Traktor Chelyabinsk': None,
                    'Avtomobilist Yekaterinburg': None,
                    'Lada Togliatti': None,
                },
                'Chernyshev': {
                    'Salavat Yulaev Ufa': None,
                    'Avangard Omsk': None,
                    'Barys Astana': None,
                    'Sibir Novosibirsk': None,
                    'Amur Khabarovsk': None,
                    'Metallurg Novokuznetsk': None,
                }
            }
        },
        '2010-2011': {
            'Western Conference': {
                'Bobrov': {
                    'UHC Dynamo': None,
                    'SKA Saint Petersburg': None,
                    'Spartak Moscow': None,
                    'Dinamo Riga': None,
                    'CSKA Moscow': None,
                },
                'Tarasov': {
                    'Lokomotiv Yaroslavl': None,
                    'Atlant Moscow Oblast': None,
                    'Severstal Cherepovets': None,
                    'Dinamo Minsk': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Vityaz Chekhov': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Ak Bars Kazan': None,
                    'Metallurg Magnitogorsk': None,
                    'Yugra Khanty-Mansiysk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Traktor Chelyabinsk': None,
                    'Avtomobilist Yekaterinburg': None,
                },
                'Chernyshev': {
                    'Avangard Omsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Sibir Novosibirsk': None,
                    'Barys Astana': None,
                    'Amur Khabarovsk': None,
                    'Metallurg Novokuznetsk': None,
                }
            }
        },
        '2011-2012': {
            'Western Conference': {
                'Bobrov': {
                    'SKA Saint Petersburg': None,
                    'Dynamo Moscow': None,
                    'Dinamo Riga': None,
                    'CSKA Moscow': None,
                    'Spartak Moscow': None,
                    'Lev Poprad': None,
                },
                'Tarasov': {
                    'Torpedo Nizhny Novgorod': None,
                    'Atlant Moscow Oblast': None,
                    'Severstal Cherepovets': None,
                    'Dinamo Minsk': None,
                    'Vityaz Chekhov': None,
                    'Lokomotiv Yaroslavl': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Traktor Chelyabinsk': None,
                    'Metallurg Magnitogorsk': None,
                    'Ak Bars Kazan': None,
                    'Yugra Khanty-Mansiysk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Avtomobilist Yekaterinburg': None,
                },
                'Chernyshev': {
                    'Avangard Omsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Barys Astana': None,
                    'Amur Khabarovsk': None,
                    'Metallurg Novokuznetsk': None,
                    'Sibir Novosibirsk': None,
                }
            }
        },
        '2012-2013': {
            'Western Conference': {
                'Bobrov': {
                    'SKA Saint Petersburg': None,
                    'Dynamo Moscow': None,
                    'Slovan Bratislava': None,
                    'Lev Prague': None,
                    'HC Donbass': None,
                    'Vityaz Chekhov': None,
                    'Dinamo Riga': None,
                },
                'Tarasov': {
                    'CSKA Moscow': None,
                    'Lokomotiv Yaroslavl': None,
                    'Severstal Cherepovets': None,
                    'Atlant Moscow Oblast': None,
                    'Dinamo Minsk': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Spartak Moscow': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Ak Bars Kazan': None,
                    'Traktor Chelyabinsk': None,
                    'Metallurg Magnitogorsk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Yugra Khanty-Mansiysk': None,
                    'Avtomobilist Yekaterinburg': None,
                },
                'Chernyshev': {
                    'Avangard Omsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Barys Astana': None,
                    'Sibir Novosibirsk': None,
                    'Metallurg Novokuznetsk': None,
                    'Amur Khabarovsk': None,
                }
            }
        },
        '2013-2014': {
            'Western Conference': {
                'Bobrov': {
                    'SKA Saint Petersburg': None,
                    'HC Lev Praha': None,
                    'Dinamo Riga': None,
                    'Medvescak Zagreb': None,
                    'CSKA Moscow': None,
                    'Slovan Bratislava': None,
                    'Dinamo Minsk': None,
                },
                'Tarasov': {
                    'Dynamo Moscow': None,
                    'HC Donbass': None,
                    'Lokomotiv Yaroslavl': None,
                    'Atlant Moscow Oblast': None,
                    'Severstal Cherepovets': None,
                    'Spartak Moscow': None,
                    'Vityaz Podolsk': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Metallurg Magnitogorsk': None,
                    'Ak Bars Kazan': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Avtomobilist Yekaterinburg': None,
                    'Traktor Chelyabinsk': None,
                    'Yugra Khanty-Mansiysk': None,
                    'Neftekhimik Nizhnekamsk': None,
                },
                'Chernyshev': {
                    'Barys Astana': None,
                    'Salavat Yulaev Ufa': None,
                    'Sibir Novosibirsk': None,
                    'Admiral Vladivostok': None,
                    'Avangard Omsk': None,
                    'Metallurg Novokuznetsk': None,
                    'Amur Khabarovsk': None,
                }
            }
        },
        '2014-2015': {
            'Western Conference': {
                'Bobrov': {
                    'Jokerit': None,
                    'Dinamo Minsk': None,
                    'Dinamo Riga': None,
                    'Atlant Moscow Oblast': None,
                    'Medvescak Zagreb': None,
                    'SKA Saint Petersburg': None,
                    'Slovan Bratislava': None,
                },
                'Tarasov': {
                    'Torpedo Nizhny Novgorod': None,
                    'CSKA Moscow': None,
                    'Dynamo Moscow': None,
                    'Lokomotiv Yaroslavl': None,
                    'Severstal Cherepovets': None,
                    'HC Sochi': None,
                    'Vityaz Podolsk': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Ak Bars Kazan': None,
                    'Avtomobilist Yekaterinburg': None,
                    'Yugra Khanty-Mansiysk': None,
                    'Metallurg Magnitogorsk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Lada Togliatti': None,
                    'Traktor Chelyabinsk': None,
                },
                'Chernyshev': {
                    'Admiral Vladivostok': None,
                    'Amur Khabarovsk': None,
                    'Avangard Omsk': None,
                    'Barys Astana': None,
                    'Metallurg Novokuznetsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Sibir Novosibirsk': None,
                }
            }
        },
        '2015-2016': {
            'Western Conference': {
                'Bobrov': {
                    'Dinamo Minsk': None,
                    'Dinamo Riga': None,
                    'Jokerit': None,
                    'Medvescak Zagreb': None,
                    'SKA Saint Petersburg': None,
                    'Slovan Bratislava': None,
                    'Spartak Moscow': None,
                },
                'Tarasov': {
                    'CSKA Moscow': None,
                    'Dynamo Moscow': None,
                    'HC Sochi': None,
                    'Lokomotiv Yaroslavl': None,
                    'Severstal Cherepovets': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Vityaz Podolsk': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Ak Bars Kazan': None,
                    'Avtomobilist Yekaterinburg': None,
                    'Lada Togliatti': None,
                    'Metallurg Magnitogorsk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Traktor Chelyabinsk': None,
                    'Yugra Khanty-Mansiysk': None,
                },
                'Chernyshev': {
                    'Admiral Vladivostok': None,
                    'Amur Khabarovsk': None,
                    'Avangard Omsk': None,
                    'Barys Astana': None,
                    'Metallurg Novokuznetsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Sibir Novosibirsk': None,
                }
            }
        },
        '2016-2017': {
            'Western Conference': {
                'Bobrov': {
                    'Dinamo Minsk': None,
                    'Dinamo Riga': None,
                    'Jokerit': None,
                    'Medvescak Zagreb': None,
                    'SKA Saint Petersburg': None,
                    'Slovan Bratislava': None,
                    'Spartak Moscow': None,
                },
                'Tarasov': {
                    'CSKA Moscow': None,
                    'Dynamo Moscow': None,
                    'HC Sochi': None,
                    'Lokomotiv Yaroslavl': None,
                    'Severstal Cherepovets': None,
                    'Torpedo Nizhny Novgorod': None,
                    'Vityaz Podolsk': None,
                }
            },
            'Eastern Conference': {
                'Kharlamov': {
                    'Ak Bars Kazan': None,
                    'Avtomobilist Yekaterinburg': None,
                    'Lada Togliatti': None,
                    'Metallurg Magnitogorsk': None,
                    'Neftekhimik Nizhnekamsk': None,
                    'Traktor Chelyabinsk': None,
                    'Yugra Khanty-Mansiysk': None,
                },
                'Chernyshev': {
                    'Admiral Vladivostok': None,
                    'Amur Khabarovsk': None,
                    'Avangard Omsk': None,
                    'Barys Astana': None,
                    'Metallurg Novokuznetsk': None,
                    'Salavat Yulaev Ufa': None,
                    'Sibir Novosibirsk': None,
                    'Kunlun Red Star': None,
                }
            }
        },
    }
}

TEAM_ALIASES = {
    'Atlant Mytishi': 'Atlant Moscow Oblast',
    'Bars Kazan': 'Ak Bars Kazan',
    'Cherepovets': 'Severstal Cherepovets',
    'Din. Minsk': 'Dinamo Minsk',
    'Donbass': 'HC Donbass',
    'Dyn. Moscow': 'Dynamo Moscow',
    'HC Lev': 'Lev Poprad',
    'HC Yugra': 'Yugra Khanty-Mansiysk',
    'Khimik': 'Khimik Voskresensk',
    'Kunlun': 'Kunlun Red Star',
    'Lada': 'Lada Togliatti',
    'MVD Balashikha': 'HC MVD',
    'Nizhny Novgorod': 'Torpedo Nizhny Novgorod',
    'Niznekamsk': 'Neftekhimik Nizhnekamsk',
    'Podolsk': 'Vityaz Podolsk',
    'Salavat Ufa': 'Salavat Yulaev Ufa',
    'SKA St. Petersburg': 'SKA Saint Petersburg',
    'Sochi': 'HC Sochi',
    'Sp. Moscow': 'Spartak Moscow',
    'Tractor Chelyabinsk': 'Traktor Chelyabinsk',
    'Vladivostok': 'Admiral Vladivostok',
    'Yekaterinburg': 'Avtomobilist Yekaterinburg',
}

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
            
    if len(result) == 0:
        raise Exception("no data found in file '" + filepath + "'")
    else:
        return result


def insert_match(competition, date, home_team_id, away_team_id, full_time_home_goals, full_time_away_goals, 
                 extra_time_home_goals, extra_time_away_goals, penalties_home_goals, penalties_away_goals, cancelled, awarded, stage):
    cur = conn.cursor()
    
    cur.execute('''SELECT id FROM match WHERE "date" = ? AND home_team = ? AND away_team = ?''', (date, home_team_id, away_team_id))
    
    result = cur.fetchone()
    if result:
        matchid = result[0]
    else:
        cur.execute('''INSERT INTO match (competition, "date", home_team, away_team, 
                       full_time_home_team_goals, full_time_away_team_goals, 
                       extra_time_home_team_goals, extra_time_away_team_goals,
                       penalties_home_team_goals, penalties_away_team_goals,
                       cancelled, awarded, stage) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                    (competition, date, home_team_id, away_team_id, 
                     full_time_home_goals, full_time_away_goals, 
                     extra_time_home_goals, extra_time_away_goals, 
                     penalties_home_goals, penalties_away_goals, 
                     cancelled, awarded, stage))
        matchid = cur.lastrowid
    
    return matchid


def get_competition_id(league, season):
    cur = conn.cursor()
    
    cur.execute('''SELECT competition.id 
                   FROM competition, league, season
                   WHERE competition.league = league.id
                   AND competition.season = season.id
                   AND league.title = ?
                   AND season.title = ?''', (league, season))
                   
    return cur.fetchone()[0]


def add_competitions_and_teams():
    cur = conn.cursor()
    
    # Leagues
    for league in TEAMS:
        cur.execute('''SELECT id FROM league WHERE title = ?''', (league,))
        result = cur.fetchone()
        if result:
            league_id = result[0]
        else:
            cur.execute('''INSERT INTO league (title) VALUES (?)''', (league,))
            league_id = cur.lastrowid
    
        # Seasons
        for season in TEAMS[league]:
            cur.execute('''SELECT id FROM season WHERE title = ?''', (season,))
            result = cur.fetchone()
            if result:
                season_id = result[0]
            else:
                cur.execute('''INSERT INTO season (title) VALUES (?)''', (season,))
                season_id = cur.lastrowid
                
            # Insert competition
            cur.execute('''SELECT id FROM competition WHERE league = ? AND season = ?''', (league_id, season_id))
            result = cur.fetchone()
            if result:
                competition_id = result[0]
            else:
                cur.execute('''INSERT INTO competition (title, league, season) VALUES (?,?,?)''', (league + " " + season, league_id, season_id))
                competition_id = cur.lastrowid

            # Conferences
            for conference in TEAMS[league][season]:
                cur.execute('''SELECT id FROM conference WHERE title = ? AND competition = ?''', (conference, competition_id))
                result = cur.fetchone()
                if result:
                    conference_id = result[0]
                else:
                    cur.execute('''INSERT INTO conference (title, competition) VALUES (?,?)''', (conference, competition_id))
                    conference_id = cur.lastrowid
                    
                # Divisions
                for division in TEAMS[league][season][conference]:
                    cur.execute('''SELECT id FROM division WHERE title = ? AND conference = ?''', (division, conference_id))
                    result = cur.fetchone()
                    if result:
                        division_id = result[0]
                    else:
                        cur.execute('''INSERT INTO division (title, conference) VALUES (?,?)''', (division, conference_id))
                        division_id = cur.lastrowid
                        
                    # Teams
                    for team in TEAMS[league][season][conference][division]:
                        cur.execute('''SELECT id FROM team WHERE title = ?''', (team,))
                        result = cur.fetchone()
                        if result:
                            team_id = result[0]
                        else:
                            cur.execute('''INSERT INTO team (title) VALUES (?)''', (team,))
                            team_id = cur.lastrowid
                            
                        cur.execute('''SELECT * FROM team_division WHERE team = ? AND division = ?''', (team_id, division_id))
                        result = cur.fetchone()
                        if not result:
                            cur.execute('''INSERT INTO team_division (team, division) VALUES (?,?)''', (team_id, division_id))

def get_team_id(team_name):
    cur = conn.cursor()
    cur.execute('''SELECT id FROM team WHERE title = ?''', (team_name,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        raise Exception("No team found '%s'" % team_name)


def insert_odds(matchid, booker, home_win, draw, away_win):
    cur = conn.cursor()
    cur.execute('''SELECT * FROM odds_1X2 WHERE match = ? AND booker = ?''', (matchid, booker))
    
    result = cur.fetchone()
    
    if result:
        odds_id = result[0]
    else:
        cur.execute('''INSERT INTO odds_1X2 (match, booker, home_win, draw, away_win) VALUES (?,?,?,?,?)''', (matchid, booker, home_win, draw, away_win))
        odds_id = cur.lastrowid
        
    return odds_id


if __name__ == "__main__":

    add_competitions_and_teams()

    for filename in [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]:

        stage = None
        if 'regular_season' in filename:
            stage = 'Regular Season'
        elif 'playoffs' in filename:
            stage = 'Playoffs'
        else:
            raise Exception('Could not determine stage')

        season = filename.rsplit('_', 1)[1].split('.')[0]
        season = str(int(season.split('-')[0])) + '-' + str(int(season.split('-')[1]))

        print season

        competition_id = get_competition_id('KHL', season)
        
        filepath = os.path.join(DATA_PATH, filename)
        
        for row in read_data(filepath):
            
            date = row['date']
            
            # Get team names.
            if row['home_team'] in TEAM_ALIASES:
                home_team = TEAM_ALIASES[row['home_team']]
            else:
                home_team = row['home_team']
            if row['away_team'] in TEAM_ALIASES:
                away_team = TEAM_ALIASES[row['away_team']]
            else:
                away_team = row['away_team']
            
            # Get database id of the home team
            home_team_id = get_team_id(home_team)
            away_team_id = get_team_id(away_team)
            assert type(home_team_id) is int
            assert type(away_team_id) is int
            
            # Insert match information.
            matchid = insert_match(competition=competition_id, date=date, home_team_id=home_team_id, away_team_id=away_team_id, 
                                   full_time_home_goals=row['full_time_home_goals'], full_time_away_goals=row['full_time_away_goals'], 
                                   extra_time_home_goals=row['extra_time_home_goals'], extra_time_away_goals=row['extra_time_away_goals'], 
                                   penalties_home_goals=row['penalties_home_goals'], penalties_away_goals=row['penalties_away_goals'], 
                                   cancelled=row['cancelled'], awarded=row['awarded'], stage=stage)
            
            # Insert odds.
            insert_odds(matchid, 'HIGHEST', row['home_win_odds'], row['draw_odds'], row['away_win_odds'])
        
    conn.commit()
