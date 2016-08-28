DROP TABLE IF EXISTS odds_1X2;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS team_division;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS division;
DROP TABLE IF EXISTS conference;
DROP TABLE IF EXISTS competition;
DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS league;

CREATE TABLE league (
  id serial,
  title text NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (title)
);

CREATE TABLE season (
  id serial,
  title text NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (title)
);

CREATE TABLE competition (
  id serial,
  title text,
  league integer,
  season integer,
  PRIMARY KEY (id),
  UNIQUE (title),
  FOREIGN KEY (league) REFERENCES league(id),
  FOREIGN KEY (season) REFERENCES season(id)
);

CREATE TABLE conference (
  id serial,
  title text,
  competition integer,
  PRIMARY KEY (id),
  UNIQUE (title, competition),
  FOREIGN KEY (competition) REFERENCES competition(id)
);

CREATE TABLE division (
  id serial,
  title text,
  conference integer,
  PRIMARY KEY (id),
  UNIQUE (title, conference),
  FOREIGN KEY (conference) REFERENCES conference(id)
);

CREATE TABLE team (
  id serial,
  title text NOT NULL,
  aliases text,
  PRIMARY KEY (id),
  UNIQUE (title)
);

CREATE TABLE team_division (
  team serial,
  division integer,
  PRIMARY KEY (team, division),
  FOREIGN KEY (team) REFERENCES team(id),
  FOREIGN KEY (division) REFERENCES division(id)
);

CREATE TABLE match (
  id serial,
  competition integer NOT NULL, 
  "date" text NOT NULL,
  home_team integer NOT NULL,
  away_team integer NOT NULL,
  full_time_home_team_goals integer,
  full_time_away_team_goals integer,
  extra_time_home_team_goals integer,
  extra_time_away_team_goals integer,
  penalties_home_team_goals integer,
  penalties_away_team_goals integer,
  awarded boolean NOT NULL DEFAULT FALSE,
  cancelled boolean NOT NULL DEFAULT FALSE,
  stage text,
  PRIMARY KEY (id),
  UNIQUE ("date", home_team, away_team),
  FOREIGN KEY (competition) REFERENCES competition(id),
  FOREIGN KEY (home_team) REFERENCES team(id),
  FOREIGN KEY (away_team) REFERENCES team(id)
);

CREATE TABLE odds_1X2 (
  "match" integer,
  booker text,
  home_win real NOT NULL,
  draw real NOT NULL,
  away_win real NOT NULL,
  PRIMARY KEY ("match", booker)
);
