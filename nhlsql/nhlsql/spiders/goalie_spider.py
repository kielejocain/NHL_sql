# These spiders crawl the NHL Individual Stats pages.
# This is compliant with the NHL stats pages as of August, 2015.
# Each spider crawls a different goalie category as controlled by
# Player's Position > Category > Report.
#
# Each spider is called as follows (if not given, is_playoffs defaults to false):
# scrapy crawl <spider name> -a season="<end year>" -a is_playoffs="true"
# E.g., to get the regular season summary data from the 1997-1998 season:
# scrapy crawl skatsum -a season="1998"
# for the playoff summary data:
# scrapy crawl skatsum -a season="1998" -a is_playoffs="true"
##################################################################

import json

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider

from nhlsql.goalie_items import *


class GoalSumSpider(CrawlSpider):
    """
    Crawls 'Goalies > Record > Summary' pages for one regular season or playoff.
    """

    # define class variables
    name = "goalsum"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalSumSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goaliesummary?cayenneExp=seasonId={}{} and '
             'gameTypeId={} and playerPositionCode="G"'.format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalSumItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalSumItem()
            goalie['nhl_num'] = row['playerId']
            # add in season data manually
            goalie['season'] = str(self.year)
            goalie['games_played'] = row['gamesPlayed']
            goalie['games_started'] = row['gamesStarted']
            goalie['wins'] = row['wins']
            goalie['losses'] = row['losses']
            goalie['ties'] = row['ties']
            goalie['ot_losses'] = row['otLosses']
            goalie['shutouts'] = row['shutouts']
            goalie['shots_against'] = row['shotsAgainst']
            goalie['goals_against'] = row['goalsAgainst']
            if row['shotsAgainst'] is not None and row['goalsAgainst'] is not None:
                goalie['saves_'] = row['shotsAgainst'] - row['goalsAgainst']
            else:
                goalie['saves_'] = None
            if goalie['saves_'] is not None:
                goalie['save_pct'] = float(goalie['saves_']) / row['shotsAgainst']
            else:
                goalie['save_pct'] = None
            goalie['toi'] = row['timeOnIce']
            if row['goalsAgainst'] is not None and row['timeOnIce'] is not None:
                goalie['gaa'] = float(3600 * row['goalsAgainst']) / row['timeOnIce']
            else:
                goalie['gaa'] = None

            # feed item to pipeline
            yield goalie


class GoalBioSpider(CrawlSpider):
    """
    Crawls 'Goalies > Record > Bios' pages for one regular season or playoff.
    """

    # define class variables
    name = "goalbio"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalBioSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goaliebios?cayenneExp=seasonId={}{} and '
             'gameTypeId={} and playerPositionCode="G"'.format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalBioItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalBioItem()
            goalie['first_name'] = row['playerName'].split()[0]
            goalie['last_name'] = row['playerName'].split()[1]
            goalie['nhl_num'] = row['playerId']
            goalie['position'] = 'G'
            goalie['birthday'] = row['playerBirthDate']
            goalie['draft_year'] = row['playerDraftYear']
            goalie['draft_position'] = row['playerDraftOverallPickNo']

            # feed item to pipeline
            yield goalie


class GoalESSpider(CrawlSpider):
    """
    Crawls 'Goalies > Special Teams > Even Stength' pages for one regular season or playoff.
    """

    # define class variables
    name = "goales"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalESSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goalieevenstrength?cayenneExp=seasonId={}{} and '
             'gameTypeId={} and playerPositionCode="G"'.format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalESItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalESItem()
            goalie['nhl_num'] = row['playerId']
            # add in season data manually
            goalie['season'] = str(self.year)
            goalie['es_shots_against'] = row['evShotsAgainst']
            goalie['es_goals_against'] = row['evGoalsAgainst']
            goalie['es_saves'] = row['evSaves']
            if goalie['es_saves'] > 0 and goalie['es_shots_against'] > 0:
                goalie['es_save_pct'] = float(goalie['es_saves']) / goalie['es_shots_against']
            else:
                goalie['es_save_pct'] = None

            # feed item to pipeline
            yield goalie


class GoalPPSpider(CrawlSpider):
    """
    Crawls 'Goalies > Special Teams > Power Play' pages for one regular season or playoff.
    """

    # define class variables
    name = "goalpp"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalPPSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goaliepowerplay?cayenneExp=seasonId={}{} and '
             'gameTypeId={} and playerPositionCode="G"'.format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalPPItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalPPItem()
            goalie['nhl_num'] = row['playerId']
            # add in season data manually
            goalie['season'] = str(self.year)
            goalie['pp_shots_against'] = row['ppShotsAgainst']
            goalie['pp_goals_against'] = row['ppGoalsAgainst']
            goalie['pp_saves'] = row['ppSaves']
            if goalie['pp_saves'] > 0 and goalie['pp_shots_against'] > 0:
                goalie['pp_save_pct'] = float(goalie['pp_saves']) / goalie['pp_shots_against']
            else:
                goalie['pp_save_pct'] = None

            # feed item to pipeline
            yield goalie


class GoalSHSpider(CrawlSpider):
    """
    Crawls 'Goalies > Special Teams > Penalty Kill' pages for one regular season or playoff.
    """

    # define class variables
    name = "goalsh"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalSHSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goaliepenaltykill?cayenneExp=seasonId={}{} and '
             'gameTypeId={} and playerPositionCode="G"'.format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalSHItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalSHItem()
            goalie['nhl_num'] = row['playerId']
            # add in season data manually
            goalie['season'] = str(self.year)
            goalie['sh_shots_against'] = row['shShotsAgainst']
            goalie['sh_goals_against'] = row['shGoalsAgainst']
            goalie['sh_saves'] = row['shSaves']
            if goalie['sh_saves'] > 0 and goalie['sh_shots_against'] > 0:
                goalie['sh_save_pct'] = float(goalie['sh_saves']) / goalie['sh_shots_against']
            else:
                goalie['sh_save_pct'] = None

            # feed item to pipeline
            yield goalie


class GoalSOSpider(CrawlSpider):
    """
    Crawls 'Goalies > Special Teams > Shootout' pages for one regular season or playoff.
    """

    # define class variables
    name = "goalso"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalSOSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/shootouts/season/goalieshootout'
             '?cayenneExp=seasonId={}{} and gameTypeId={} and playerPositionCode="G"'.
             format(self.year - 1, self.year, self.game_type)
             )
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalSOItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            goalie = GoalSOItem()
            goalie['nhl_num'] = row['playerId']
            # add in season data manually
            goalie['season'] = str(self.year)
            goalie['so_wins'] = row['shootoutGamesWon']
            goalie['so_losses'] = row['shootoutGamesLost']
            goalie['so_shots_against'] = row['shootoutShotsAgainst']
            goalie['so_goals_against'] = row['shootoutGoals']
            goalie['so_saves'] = goalie['so_shots_against'] - goalie['so_goals_against']
            if goalie['so_saves'] > 0 and goalie['so_shots_against'] > 0:
                goalie['so_save_pct'] = float(goalie['so_saves']) / goalie['so_shots_against']
            else:
                goalie['so_save_pct'] = None

            # feed item to pipeline
            yield goalie


class GoalTeamSpider(CrawlSpider):
    """Crawls 'Goalies > Records > Bios' pages for one regular season or playoff, obtaining only teams played for."""
    name = "goalteam"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(GoalTeamSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ('http://www.nhl.com/stats/rest/grouped/goalies/season/goaliebios?cayenneExp=seasonId={}{}'
             ' and gameTypeId={} and playerPositionCode="G"').format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields GoalTeamItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            teams = row['playerTeamsPlayedFor'].split(", ")
            for i, team in enumerate(teams):
                goalie = GoalTeamItem()
                goalie['nhl_num'] = row['playerId']
                # add in season data manually
                goalie['season'] = str(self.year)
                goalie['order'] = i
                goalie['team'] = team
                if i == len(teams) - 1:
                    goalie['current'] = True
                else:
                    goalie['current'] = False

                # feed item to pipeline
                yield goalie
