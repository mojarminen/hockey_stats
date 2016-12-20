# -*- coding: utf-8 -*-
import sys

import history

SEASON = '2016-2017'
LEAGUE = 'SM-LIIGA'

def output(home, away):
    HOME_TEAM = home
    AWAY_TEAM = away

    common_percentages = history.get_full_time_1X2_percentages(LEAGUE, SEASON)
    print 'COMMON:', common_percentages
    print

    home_team_match_percentages = history.get_full_time_match_percentages_of_team(HOME_TEAM, LEAGUE, SEASON)
    home_team_home_match_percentages = history.get_full_time_home_match_percentages_of_team(HOME_TEAM, LEAGUE, SEASON)
    print 'HOME:'
    print 'home matches:', home_team_home_match_percentages
    print 'all matches:', home_team_match_percentages
    print

    away_team_match_percentages = history.get_full_time_match_percentages_of_team(AWAY_TEAM, LEAGUE, SEASON)
    away_team_away_match_percentages = history.get_full_time_away_match_percentages_of_team(AWAY_TEAM, LEAGUE, SEASON)
    print 'AWAY:'
    print 'away matches:', away_team_away_match_percentages
    print 'all matches:', away_team_match_percentages
    print

    est_home_win = (common_percentages[0] + home_team_match_percentages[0] + home_team_home_match_percentages[0] + away_team_away_match_percentages[2] + away_team_match_percentages[2]) / 5
    est_away_win = (common_percentages[2] + home_team_match_percentages[2] + home_team_home_match_percentages[2] + away_team_away_match_percentages[0] + away_team_match_percentages[0]) / 5
    est_draw = 1.0-est_home_win-est_away_win
    print 'ESTIMATION:', (est_home_win, est_draw, est_away_win)
    print 'ODD LIMITS:', (1/est_home_win, 1/est_draw, 1/est_away_win)

if __name__ == '__main__':
    home = unicode(sys.argv[1], 'utf-8')
    away = unicode(sys.argv[2], 'utf-8')
    output(home, away)
