from sqlalchemy import create_engine, Column, Date, Integer, String, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_skater_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class SkaterSum(DeclarativeBase):
    """Sqlalchemy skater summary model"""
    __tablename__ = 'skatsum'

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    games_played = Column('games_played', Integer)
    goals = Column('goals', Integer)
    assists = Column('assists', Integer)
    points = Column('points', Integer)
    plus_minus = Column('plus_minus', Integer)
    gw_goals = Column('gw_goals', Integer)
    ot_goals = Column('ot_goals', Integer)
    shots = Column('shots', Integer)
    shot_pct = Column('shot_pct', Numeric)


class SkaterPP(DeclarativeBase):
    """Sqlalchemy skater powerplay model"""
    __tablename__ = 'skatpp'

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    pp_goals = Column('pp_goals', Integer)
    pp_assists = Column('pp_assists', Integer)
    pp_points = Column('pp_points', Integer)
    pp_shots = Column('pp_shots', Integer)
    pp_shot_pct = Column('pp_shot_pct', Numeric)
    pp_hits = Column('pp_hits', Integer)
    pp_shots_blocked = Column('pp_shots_blocked', Integer)
    pp_missed_shots = Column('pp_missed_shots', Integer)
    pp_giveaways = Column('pp_giveaways', Integer)
    pp_takeaways = Column('pp_takeaways', Integer)
    pp_faceoff_wins = Column('pp_faceoff_wins', Integer)
    pp_faceoff_losses = Column('pp_faceoff_losses', Integer)
    pp_faceoff_pct = Column('pp_faceoff_pct', Numeric)


class SkaterSH(DeclarativeBase):
    """Sqlalchemy skater penalty kill model"""
    __tablename__ = 'skatsh'

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    sh_goals = Column('sh_goals', Integer)
    sh_assists = Column('sh_assists', Integer)
    sh_points = Column('sh_points', Integer)
    sh_shots = Column('sh_shots', Integer)
    sh_shot_pct = Column('sh_shot_pct', Numeric)
    sh_hits = Column('sh_hits', Integer)
    sh_shots_blocked = Column('sh_shots_blocked', Integer)
    sh_missed_shots = Column('sh_missed_shots', Integer)
    sh_giveaways = Column('sh_giveaways', Integer)
    sh_takeaways = Column('sh_takeaways', Integer)
    sh_faceoff_wins = Column('sh_faceoff_wins', Integer)
    sh_faceoff_losses = Column('sh_faceoff_losses', Integer)
    sh_faceoff_pct = Column('sh_faceoff_pct', Numeric)


class SkaterSO(DeclarativeBase):
    """Sqlalchemy skater penalty kill model"""
    __tablename__ = 'skatso'

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    so_shots = Column('so_shots', Integer)
    so_goals = Column('so_goals', Integer)
    so_pct = Column('so_pct', Numeric)


class SkaterPM(DeclarativeBase):
    """Sqlalchemy skater plus/minus model"""
    __tablename__ = "skatpm"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    team_goals_for = Column('team_goals_for', Integer)
    team_pp_goals_for = Column('team_pp_goals_for', Integer)
    team_goals_against = Column('team_goals_against', Integer)
    team_pp_goals_against = Column('team_pp_goals_against', Integer)


class SkaterRTS(DeclarativeBase):
    """Sqlalchemy skater real-time stats model"""
    __tablename__ = "skatrts"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    hits = Column('hits', Integer)
    shots_blocked = Column('shots_blocked', Integer)
    missed_shots = Column('missed_shots', Integer)
    giveaways = Column('giveaways', Integer)
    takeaways = Column('takeaways', Integer)
    faceoff_wins = Column('faceoff_wins', Integer)
    faceoff_losses = Column('faceoff_losses', Integer)
    faceoff_pct = Column('faceoff_pct', Numeric)


class SkaterPIM(DeclarativeBase):
    """Sqlalchemy skater penalty model"""
    __tablename__ = "skatpim"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    minors = Column('minors', Integer)
    majors = Column('majors', Integer)
    misconducts = Column('misconducts', Integer)
    game_misconducts = Column('game_misconducts', Integer)
    matches = Column('matches', Integer)
    penalty_minutes = Column('penalty_minutes', Integer)


class SkaterTOI(DeclarativeBase):
    """Sqlalchemy skater time on ice model"""
    __tablename__ = "skattoi"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    es_toi = Column('es_toi', Integer)
    pp_toi = Column('pp_toi', Integer)
    sh_toi = Column('sh_toi', Integer)
    toi = Column('toi', Integer)


class GoalieSum(DeclarativeBase):
    """Sqlalchemy goalie summary model"""
    __tablename__ = "goalsum"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    games_played = Column('games_played', Integer)
    games_started = Column('games_started', Integer)
    wins = Column('wins', Integer)
    losses = Column('losses', Integer)
    ties = Column('ties', Integer)
    ot_losses = Column('ot_losses', Integer)
    shutouts = Column('shutouts', Integer)
    shots_against = Column('shots_against', Integer)
    goals_against = Column('goals_against', Integer)
    saves_ = Column('saves', Integer)
    save_pct = Column('save_pct', Numeric)
    toi = Column('toi', Integer)
    gaa = Column('gaa', Numeric)


class GoalieES(DeclarativeBase):
    """Sqlalchemy goalie even strength model"""
    __tablename__ = "goales"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    es_shots_against = Column('es_shots_against', Integer)
    es_goals_against = Column('es_goals_against', Integer)
    es_saves = Column('es_saves', Integer)
    es_save_pct = Column('es_save_pct', Numeric)


class GoaliePP(DeclarativeBase):
    """Sqlalchemy goalie power play model"""
    __tablename__ = "goalpp"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    pp_shots_against = Column('pp_shots_against', Integer)
    pp_goals_against = Column('pp_goals_against', Integer)
    pp_saves = Column('pp_saves', Integer)
    pp_save_pct = Column('pp_save_pct', Numeric)


class GoalieSH(DeclarativeBase):
    """Sqlalchemy goalie penalty kill model"""
    __tablename__ = "goalsh"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    sh_shots_against = Column('sh_shots_against', Integer)
    sh_goals_against = Column('sh_goals_against', Integer)
    sh_saves = Column('sh_saves', Integer)
    sh_save_pct = Column('sh_save_pct', Numeric)


class GoalieSO(DeclarativeBase):
    """Sqlalchemy goalie shootout model"""
    __tablename__ = "goalso"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    so_wins = Column('so_wins', Integer)
    so_losses = Column('so_losses', Integer)
    so_shots_against = Column('so_shots_against', Integer)
    so_goals_against = Column('so_goals_against', Integer)
    so_saves = Column('so_saves', Integer)
    so_save_pct = Column('so_save_pct', Numeric)


class PlayerBio(DeclarativeBase):
    """Sqlalchemy skater bio model"""
    __tablename__ = "players"

    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    nhl_num = Column('nhl_num', Integer, primary_key=True)
    position = Column('player_position', String)
    birthday = Column('birthday', Date)
    draft_year = Column('draft_year', Integer, nullable=True)
    draft_position = Column('draft_position', Integer, nullable=True)


class PlayerTeam(DeclarativeBase):
    """Sqlalchemy player team model"""
    __tablename__ = "playerteams"

    id = Column(Integer, primary_key=True)
    nhl_num = Column('nhl_num', Integer)
    season = Column('season', Integer)
    order = Column('order', Integer)
    team = Column('team', String)
    current = Column('current', Boolean)


class StandingsModel(DeclarativeBase):
    """Sqlalchemy team standings model"""
    __tablename__ = "standings"

    team = Column('team', String, primary_key=True)
    division = Column('division', String)
    games_played = Column('games_played', Integer)
    wins = Column('wins', Integer)
    losses = Column('losses', Integer)
    ot_losses = Column('ot_losses', Integer)
    points = Column('points', Integer)
    row = Column('row', Integer)
