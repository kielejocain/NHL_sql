# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GoalSumItem(Item):
    # define the fields for your item here like:
    # name = Field()
    first_name = Field()
    last_name = Field()
    nhl_num = Field()
    season = Field()
    player_season_id = Field()
    position = Field()
    team = Field()
    team2 = Field()
    team3 = Field()
    games_played = Field()
    games_started = Field()
    wins = Field()
    losses = Field()
    ties = Field()
    overtime_losses = Field()
    shots_against = Field()
    goals_against = Field()
    gaa = Field()
    saves_ = Field()
    save_pct = Field()
    shutouts = Field()
    goals = Field()
    assists = Field()
    penalty_minutes = Field()
    toi = Field()
    
class GoalBioItem(Item):
    nhl_num = Field()
    season = Field()
    player_season_id = Field()
    birth_year = Field()
    draft_year = Field()

class GoalPSItem(Item):
    nhl_num = Field()
    season = Field()
    player_season_id = Field()
    ps_attempts = Field()
    ps_goals_against = Field()
    ps_saves = Field()

class GoalSOItem(Item):
    nhl_num = Field()
    season = Field()
    player_season_id = Field()
    so_wins = Field()
    so_losses = Field()
    so_shots_against = Field()
    so_goals_against = Field()

class GoalSTItem(Item):
    nhl_num = Field()
    season = Field()
    player_season_id = Field()
    es_shots_against = Field()
    es_goals_against = Field()
    es_saves = Field()
    es_save_pct = Field()
    pp_shots_against = Field()
    pp_goals_against = Field()
    pp_saves = Field()
    pp_save_pct = Field()
    sh_shots_against = Field()
    sh_goals_against = Field()
    sh_saves = Field()
    sh_save_pct = Field()
