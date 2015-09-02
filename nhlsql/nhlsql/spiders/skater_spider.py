# These spiders crawl the NHL Individual Stats pages.
# This is compliant with the NHL stats pages as of August, 2015.
# Each spider crawls a different skater category as controlled by
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

from nhlsql.skater_items import *


class SkatSumSpider(CrawlSpider):
    """
    Crawls 'Skaters > Scoring > Summary' pages for one regular season or playoff.
    """

    # define class variables
    name = "skatsum"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatSumSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatSumItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatSumItem()
            skater['nhl_num'] = row['playerId']
            # WHERE IS PLUS MINUS BREAKDOWN!!!
            # add in season data manually
            skater['season'] = str(self.year)
            skater['games_played'] = row['gamesPlayed']
            skater['goals'] = row['goals']
            skater['assists'] = row['assists']
            skater['points'] = row['points']
            skater['plus_minus'] = row['plusMinus']
            skater['gw_goals'] = row['gameWinningGoals']
            skater['ot_goals'] = row['otGoals']
            skater['shots'] = row['shots']
            if row['shots'] > 0:
                skater['shot_pct'] = float(row['goals']) / row['shots']
            else:
                skater['shot_pct'] = None

            # feed item to pipeline
            yield skater


class SkatPPSpider(CrawlSpider):
    """
    Crawls 'Skaters > Special Teams > Powerplay' pages for one regular season or playoff.
    """

    # define class variables
    name = "skatpp"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatPPSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/powerplay?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatPPItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatPPItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['pp_goals'] = row['ppGoals']
            skater['pp_assists'] = row['ppAssists']
            skater['pp_points'] = row['ppPoints']
            skater['pp_shots'] = row['ppShots']
            skater['pp_hits'] = row['ppHits']
            skater['pp_blocks'] = row['ppBlockedShots']
            skater['pp_missed_shots'] = row['ppMissedShots']
            skater['pp_giveaways'] = row['ppGiveaways']
            skater['pp_takeaways'] = row['ppTakeaways']
            skater['pp_faceoff_wins'] = row['ppFaceoffsWon']
            skater['pp_faceoff_losses'] = row['ppFaceoffsLost']
            if row['ppFaceoffsWon'] + row['ppFaceoffsLost'] > 0:
                skater['pp_faceoff_pct'] = float(row['ppFaceoffsWon']) / (row['ppFaceoffsWon'] + row['ppFaceoffsLost'])
            else:
                skater['pp_faceoff_pct'] = None

            # feed item to pipeline
            yield skater


class SkatSHSpider(CrawlSpider):
    """
    Crawls 'Skaters > Special Teams > PenaltyKill' pages for one regular season or playoff.
    """

    # define class variables
    name = "skatsh"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatSHSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/penaltykill?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatSHItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatSHItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['sh_goals'] = row['shGoals']
            skater['sh_assists'] = row['shAssists']
            skater['sh_points'] = row['shPoints']
            skater['sh_shots'] = row['shShots']
            skater['sh_hits'] = row['shHits']
            skater['sh_blocks'] = row['shBlockedShots']
            skater['sh_missed_shots'] = row['shMissedShots']
            skater['sh_giveaways'] = row['shGiveaways']
            skater['sh_takeaways'] = row['shTakeaways']
            skater['sh_faceoff_wins'] = row['shFaceoffsWon']
            skater['sh_faceoff_losses'] = row['shFaceoffsLost']
            if row['shFaceoffsWon'] + row['shFaceoffsLost'] > 0:
                skater['sh_faceoff_pct'] = float(row['shFaceoffsWon']) / (row['shFaceoffsWon'] + row['shFaceoffsLost'])
            else:
                skater['sh_faceoff_pct'] = None

            # feed item to pipeline
            yield skater


class SkatSOSpider(CrawlSpider):
    """
    Crawls 'Skaters > Special Teams > Shootouts' pages for one regular season or playoff.
    """

    # define class variables
    name = "skatso"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatSOSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/shootouts/season/skatershootout?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatSOItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatSOItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['so_shots'] = row['shootoutShots']
            skater['so_goals'] = row['shootoutGoals']
            if row['shootoutShots'] > 0:
                skater['so_pct'] = float(row['shootoutGoals']) / row['shootoutShots']
            else:
                skater['so_pct'] = None

            # feed item to pipeline
            yield skater


class SkatPMSpider(CrawlSpider):
    """Crawls 'Skaters > Scoring > Plus-Minus' pages for one regular season or playoff."""
    name = "skatpm"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatPMSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/plusminus?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatPMItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatPMItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['team_goals_for'] = row['teamGoalsFor']
            skater['team_goals_against'] = row['teamGoalsAgainst']
            skater['team_pp_goals_for'] = row['ppTeamGoalsFor']
            skater['team_pp_goals_against'] = row['ppTeamGoalsAgainst']

            # feed item to pipeline
            yield skater


class SkatBioSpider(CrawlSpider):
    """Crawls 'Skaters > More... > Bios' pages for one regular season or playoff."""
    name = "skatbio"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatBioSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/bios?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatBioItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatBioItem()
            skater['first_name'] = row['playerName'].split()[0]
            skater['last_name'] = row['playerName'].split()[1]
            skater['nhl_num'] = row['playerId']
            skater['position'] = row['playerPositionCode']
            skater['birthday'] = row['playerBirthDate']
            skater['draft_year'] = row['playerDraftYear']
            skater['draft_position'] = row['playerDraftOverallPickNo']

            # feed item to pipeline
            yield skater


class SkatRTSSpider(CrawlSpider):
    """Crawls 'Skaters > More... > Real Time' pages for one regular season or playoff."""
    name = "skatrts"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatRTSSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/realtime?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatRTSItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatRTSItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['hits'] = row['hits']
            skater['blocked_shots'] = row['blockedShots']
            skater['missed_shots'] = row['missedShots']
            skater['giveaways'] = row['giveaways']
            skater['takeaways'] = row['takeaways']
            skater['faceoff_wins'] = row['faceoffsWon']
            skater['faceoff_losses'] = row['faceoffsLost']
            if row['faceoffs'] > 0:
                skater['faceoff_pct'] = float(row['faceoffsWon']) / (row['faceoffsWon'] + row['faceoffsLost'])
            else:
                skater['faceoff_pct'] = None

            # feed item to pipeline
            yield skater


class SkatPIMSpider(CrawlSpider):
    """Crawls 'Skaters > More... > Penalties' pages for one regular season or playoff."""
    name = "skatpim"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatPIMSpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/penalties?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatPIMItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatPIMItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['minors'] = row['penaltiesMinor']
            skater['majors'] = row['penaltiesMajor']
            skater['misconducts'] = row['penaltiesMisconduct']
            skater['game_misconducts'] = row['penaltiesGameMisconduct']
            skater['matches'] = row['penaltiesMatch']

            # feed item to pipeline
            yield skater


class SkatTOISpider(CrawlSpider):
    """Crawls 'Skaters > More... > Time On Ice' pages for one regular season or playoff."""
    name = "skattoi"
    allowed_domains = ["nhl.com"]
    start_urls = []

    def __init__(self, season, is_playoffs="", *args, **kwargs):
        super(SkatTOISpider, self).__init__(*args, **kwargs)

        # allows the passing of the command line argument to parse_item method
        self.year = int(season)

        # sets game_type to the URL argument required
        if is_playoffs:
            self.game_type = 3
        else:
            self.game_type = 2

        self.start_urls = [
            ("http://www.nhl.com/stats/rest/grouped/skaters/season/timeonice?cayenneExp=seasonId={}{}"
             " and gameTypeId={}").format(self.year - 1, self.year, self.game_type)
        ]

    def parse(self, response):
        """
        A generator that takes in the HMTL and parses the included JSON.
        :param response: the HTML response passed in by the spider
        :return: yields SkatTOIItem objects
        """
        sel = Selector(response)

        # collect data from HTML, converts to JSON with Python typing
        data = json.loads(sel.xpath('//p/text()').extract()[0])

        for row in data['data']:
            skater = SkatTOIItem()
            skater['nhl_num'] = row['playerId']
            # add in season data manually
            skater['season'] = str(self.year)
            skater['es_toi'] = row['evTimeOnIce']
            skater['pp_toi'] = row['ppTimeOnIce']
            skater['sh_toi'] = row['shTimeOnIce']
            skater['toi'] = row['timeOnIce']

            # feed item to pipeline
            yield skater
