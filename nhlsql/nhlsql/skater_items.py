# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SkatSumItem(Item):
    nhl_num = Field()
    season = Field()
    games_played = Field()
    goals = Field()
    assists = Field()
    points = Field()
    plus_minus = Field()
    gw_goals = Field()
    ot_goals = Field()
    shots = Field()
    shot_pct = Field()


class SkatPPItem(Item):
    nhl_num = Field()
    season = Field()
    pp_goals = Field()
    pp_assists = Field()
    pp_points = Field()
    pp_shots = Field()
    pp_shot_pct = Field()
    pp_hits = Field()
    pp_shots_blocked = Field()
    pp_missed_shots = Field()
    pp_giveaways = Field()
    pp_takeaways = Field()
    pp_faceoff_wins = Field()
    pp_faceoff_losses = Field()
    pp_faceoff_pct = Field()


class SkatSHItem(Item):
    nhl_num = Field()
    season = Field()
    sh_goals = Field()
    sh_assists = Field()
    sh_points = Field()
    sh_shots = Field()
    sh_shot_pct = Field()
    sh_hits = Field()
    sh_shots_blocked = Field()
    sh_missed_shots = Field()
    sh_giveaways = Field()
    sh_takeaways = Field()
    sh_faceoff_wins = Field()
    sh_faceoff_losses = Field()
    sh_faceoff_pct = Field()


class SkatSOItem(Item):
    nhl_num = Field()
    season = Field()
    so_shots = Field()
    so_goals = Field()
    so_pct = Field()


class SkatPMItem(Item):
    nhl_num = Field()
    season = Field()
    team_goals_for = Field()
    team_pp_goals_for = Field()
    team_goals_against = Field()
    team_pp_goals_against = Field()


class SkatBioItem(Item):
    first_name = Field()
    last_name = Field()
    nhl_num = Field()
    position = Field()
    birthday = Field()
    draft_year = Field()
    draft_position = Field()


class SkatRTSItem(Item):
    nhl_num = Field()
    season = Field()
    hits = Field()
    shots_blocked = Field()
    missed_shots = Field()
    giveaways = Field()
    takeaways = Field()
    faceoff_wins = Field()
    faceoff_losses = Field()
    faceoff_pct = Field()


class SkatPIMItem(Item):
    nhl_num = Field()
    season = Field()
    minors = Field()
    majors = Field()
    misconducts = Field()
    game_misconducts = Field()
    matches = Field()
    penalty_minutes = Field()


class SkatTOIItem(Item):
    nhl_num = Field()
    season = Field()
    es_toi = Field()
    pp_toi = Field()
    sh_toi = Field()
    toi = Field()


class SkatTeamItem(Item):
    nhl_num = Field()
    season = Field()
    order = Field()
    team = Field()
    current = Field()
