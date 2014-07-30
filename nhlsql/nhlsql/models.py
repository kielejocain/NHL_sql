from sqlalchemy import create_engine, Column, Integer, String, Numeric
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
    __tablename__ = "skatsum"

    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    team = Column('team', String)
    team2 = Column('team2', String, nullable=True)
    team3 = Column('team3', String, nullable=True)
    position = Column('position', String)
    games_played = Column('games_played', Integer)
    goals = Column('goals', Integer)
    assists = Column('assists', Integer)
    points = Column('points', Integer)
    plus_minus = Column('plus_minus', Integer)
    penalty_minutes = Column('penalty_minutes', Integer)
    pp_goals = Column('pp_goals', Integer)
    pp_points = Column('pp_points', Integer)
    sh_goals = Column('sh_goals', Integer)
    sh_points = Column('sh_points', Integer)
    gw_goals = Column('gw_goals', Integer)
    ot_goals = Column('ot_goals', Integer)
    shots = Column('shots', Integer)
    shot_pct = Column('shot_pct', Numeric)
    
class SkaterBio(DeclarativeBase):
    """Sqlalchemy skater bio model"""
    __tablename__ = "skatbio"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    birth_year = Column('birth_year', Integer)
    
class SkaterEng(DeclarativeBase):
    """Sqlalchemy skater empty net/penalty shot goals model"""
    __tablename__ = "skateng"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    en_goals = Column('en_goals', Integer)
    ps_goals = Column('ps_goals', Integer)
    
class SkaterPIM(DeclarativeBase):
    """Sqlalchemy skater penalty model"""
    __tablename__ = "skatpim"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    minors = Column('minors', Integer)
    majors = Column('majors', Integer)
    misconducts = Column('misconducts', Integer)
    game_misconducts = Column('game_misconducts', Integer)
    matches = Column('matches', Integer)
    
class SkaterPM(DeclarativeBase):
    """Sqlalchemy skater plus/minus model"""
    __tablename__ = "skatpm"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    team_goals_for = Column('team_goals_for', Integer)
    team_pp_goals_for = Column('team_pp_goals_for', Integer)
    team_goals_against = Column('team_goals_against', Integer)
    team_pp_goals_against = Column('team_pp_goals_against', Integer)
    
class SkaterRTS(DeclarativeBase):
    """Sqlalchemy skater real-time stats model"""
    __tablename__ = "skatrts"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    hits = Column('hits', Integer)
    blocked_shots = Column('blocked_shots', Integer)
    missed_shots = Column('missed_shots', Integer)
    giveaways = Column('giveaways', Integer)
    takeaways = Column('takeaways', Integer)
    faceoff_wins = Column('faceoff_wins', Integer)
    faceoff_losses = Column('faceoff_losses', Integer)
    
class SkaterSO(DeclarativeBase):
    """Sqlalchemy skater shootout model"""
    __tablename__ = "skatso"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    so_shots = Column('so_shots', Integer)
    so_goals = Column('so_goals', Integer)
    so_pct = Column('so_pct', Numeric)
    game_deciding_goals = Column('game_deciding_goals', Integer)
    
class SkaterOT(DeclarativeBase):
    """Sqlalchemy skater overtime model"""
    __tablename__ = "skatot"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    ot_games_played = Column('ot_games_played', Integer)
    ot_assists = Column('ot_assists', Integer)
    ot_points = Column('ot_points', Integer)
    
class SkaterTOI(DeclarativeBase):
    """Sqlalchemy skater time on ice model"""
    __tablename__ = "skattoi"

    nhl_num = Column('nhl_num', Integer, primary_key=True)
    season = Column('season', Integer)
    es_toi = Column('es_toi', Integer)
    sh_toi = Column('sh_toi', Integer)
    pp_toi = Column('pp_toi', Integer)
    toi = Column('toi', Integer)
    