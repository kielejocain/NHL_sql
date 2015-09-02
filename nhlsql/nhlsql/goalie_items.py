# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GoalSumItem(Item):
    # define the fields for your item here like:
    # name = Field()
    nhl_num = Field()
    season = Field()
    games_played = Field()
    games_started = Field()
    wins = Field()
    losses = Field()
    ties = Field()
    ot_losses = Field()
    shutouts = Field()
    shots_against = Field()
    goals_against = Field()
    saves_ = Field()
    save_pct = Field()
    toi = Field()
    gaa = Field()
    

class GoalBioItem(Item):
    first_name = Field()
    last_name = Field()
    nhl_num = Field()
    position = Field()
    birthday = Field()
    draft_year = Field()
    draft_position = Field()


class GoalESItem(Item):
    nhl_num = Field()
    es_shots_against = Field()
    es_goals_against = Field()
    es_saves = Field()
    es_save_pct = Field()


class GoalPPItem(Item):
    nhl_num = Field()
    pp_shots_against = Field()
    pp_goals_against = Field()
    pp_saves = Field()
    pp_save_pct = Field()


class GoalSHItem(Item):
    nhl_num = Field()
    sh_shots_against = Field()
    sh_goals_against = Field()
    sh_saves = Field()
    sh_save_pct = Field()


class GoalSOItem(Item):
    nhl_num = Field()
    season = Field()
    so_wins = Field()
    so_losses = Field()
    so_shots_against = Field()
    so_goals_against = Field()


class GoalTeamItem(Item):
    nhl_num = Field()
    season = Field()
    order = Field()
    team = Field()
    current = Field()
