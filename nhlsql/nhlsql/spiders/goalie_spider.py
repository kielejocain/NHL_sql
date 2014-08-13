# These spiders crawl the NHL Individual Stats pages.
# Each spider crawls a different goalie category ("view").

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nhlsql.goalie_items import *

# This spider grabs most classic stats from the 'Summary' pages.

class GoalSumSpider(CrawlSpider):
    name = "goalsum"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(LxmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl goalsum -a season='1998' etc...
    
    def __init__(self, season, *args, **kwargs):
        super(GoalSumSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URL procedurally
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=summary&sort=wins&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # prepare to adjust for shootout stats if necessary
        shootout = 0
        if self.year > 2005:
            shootout = 1
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(GoalSumItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # players on one (extant) team all season have link to team page
            if row.xpath('td[3]/a/text()').extract():
                loader.add_xpath('team', './/td[3]/a/text()')
                loader.add_value('team2', None)
                loader.add_value('team3', None)
            else:
                temp = row.xpath('td[3]/text()').extract()[0]
                teams = temp.split(', ')
                loader.add_value('team', teams[0])
                if len(teams) > 2:
                    loader.add_value('team2', teams[1])
                    loader.add_value('team3', teams[2])
                elif len(teams) == 2:
                    loader.add_value('team2', teams[1])
                    loader.add_value('team3', None)
                else:
                    loader.add_value('team2', None)
                    loader.add_value('team3', None)
            
            # collect several other stats
            loader.add_xpath('games_played', './/td[4]/text()')
            loader.add_xpath('games_started', './/td[5]/text()')
            loader.add_xpath('wins', './/td[6]/text()')
            loader.add_xpath('losses', './/td[7]/text()')
            if shootout:
                loader.add_value('ties', '0')
            else:
                loader.add_xpath('ties', './/td[8]/text()')
            loader.add_xpath('overtime_losses', './/td[%d]/text()' % (9-shootout,))
            loader.add_xpath('shots_against', './/td[%d]/text()' % (10-shootout,))
            loader.add_xpath('goals_against', './/td[%d]/text()' % (11-shootout,))
            loader.add_xpath('gaa', './/td[%d]/text()' % (12-shootout,))
            loader.add_xpath('saves_', './/td[%d]/text()' % (13-shootout,))
            loader.add_xpath('save_pct', './/td[%d]/text()' % (14-shootout,))
            loader.add_xpath('shutouts', './/td[%d]/text()' % (15-shootout,))
            loader.add_xpath('goals', './/td[%d]/text()' % (16-shootout,))
            loader.add_xpath('assists', './/td[%d]/text()' % (17-shootout,))
            loader.add_xpath('penalty_minutes', './/td[%d]/text()' % (18-shootout,))
            
            # convert time in ice to seconds and add
            location = 'td[%d]/text()' % (19-shootout,)
            temp = row.xpath(location).extract()[0]
            sTemp = temp.split(':')
            sTemp[0] = sTemp[0].replace(',', '')
            loader.add_value('toi', str(60*int(sTemp[0]))+sTemp[1])
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes bio pages to get the birth year of goaltenders.

class GoalBioSpider(CrawlSpider):
    name = "goalbio"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(LxmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl goalbio -a season='1998' etc...
    
    def __init__(self, season, *args, **kwargs):
        super(GoalBioSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URL procedurally
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=goalieBios&sort=player.birthCountryAbbrev&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        name = ""
        sName = []
        num = 0
        MONTHS = {'Jan': '01',
                  'Feb': '02',
                  'Mar': '03',
                  'Apr': '04',
                  'May': '05',
                  'Jun': '06',
                  'Jul': '07',
                  'Aug': '08',
                  'Sep': '09',
                  'Oct': '10',
                  'Nov': '11',
                  'Dec': '12'}
        
        # loop through players
        for row in rows:
            loader = ItemLoader(GoalBioItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # parse the name
            name = row.xpath('td[2]/a/text()').extract()
            sName = name[0].split(' ',1)
            loader.add_value('first_name', sName[0])
            loader.add_value('last_name', sName[1])
            
            # collect birth year
            bDate = row.xpath('td[4]/text()').extract()[0]
            bYear = "19" + bDate[-2:]
            bMonth = MONTHS[bDate[:3]]
            bDay = bDate[4:6]
            loader.add_value('birthday', "%s-%s-%s" % (bYear, bMonth, bDay))
            
            # add other data points
            loader.add_value('position', 'G')
            loader.add_xpath('draft_year', './/td[12]/text()')
            loader.add_xpath('draft_position', './/td[14]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes penalty shot stats.

class GoalPSSpider(CrawlSpider):
    name = "goalps"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(LxmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl goalbio -a season='1998' etc...
    
    def __init__(self, season, *args, **kwargs):
        super(GoalPSSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URL procedurally
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=penaltyShot&sort=penaltyShotsAgainst&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(GoalPSItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect additional stats
            loader.add_xpath('ps_attempts', './/td[6]/text()')
            loader.add_xpath('ps_goals_against', './/td[7]/text()')
            loader.add_xpath('ps_saves', './/td[8]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes shootout stats.

class GoalSOSpider(CrawlSpider):
    name = "goalso"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(LxmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl goalso -a season='1998' etc...
    
    def __init__(self, season, *args, **kwargs):
        super(GoalSOSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URL procedurally
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=shootouts&sort=shootoutGamesWon&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        for row in rows:
            loader = ItemLoader(GoalSOItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect additional stats
            loader.add_xpath('so_wins', './/td[14]/text()')
            loader.add_xpath('so_losses', './/td[15]/text()')
            loader.add_xpath('so_shots_against', './/td[16]/text()')
            loader.add_xpath('so_goals_against', './/td[17]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes special teams stats.

class GoalSTSpider(CrawlSpider):
    name = "goalst"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(LxmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl goalso -a season='1998' etc...
    
    def __init__(self, season, *args, **kwargs):
        super(GoalSTSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URL procedurally
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=specialTeamSaves&sort=evenStrengthSaves&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        for row in rows:
            loader = ItemLoader(GoalSTItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect additional stats
            loader.add_xpath('es_shots_against', './/td[6]/text()')
            loader.add_xpath('es_goals_against', './/td[7]/text()')
            loader.add_xpath('es_saves', './/td[8]/text()')
            loader.add_xpath('es_save_pct', './/td[9]/text()')
            loader.add_xpath('pp_shots_against', './/td[10]/text()')
            loader.add_xpath('pp_goals_against', './/td[11]/text()')
            loader.add_xpath('pp_saves', './/td[12]/text()')
            loader.add_xpath('pp_save_pct', './/td[13]/text()')
            loader.add_xpath('sh_shots_against', './/td[14]/text()')
            loader.add_xpath('sh_goals_against', './/td[15]/text()')
            loader.add_xpath('sh_saves', './/td[16]/text()')
            loader.add_xpath('sh_save_pct', './/td[17]/text()')
            
            # feed item to pipeline
            yield loader.load_item()