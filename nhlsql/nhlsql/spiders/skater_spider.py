# These spiders crawl the NHL Individual Stats pages.
# Each spider crawls a different skater category ("view").

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nhlsql.skater_items import *

# This spider grabs most classic stats from the 'Summary' pages.

class SkatSumSpider(CrawlSpider):
    #define class variables
    name = "skatsum"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatSumSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=summary&sort=points&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # prepare to adjust for shootout stats if necessary
        shootout = 0
        if self.year > 2005:
            shootout = 1
            
        # instantiate parsing variables
        name = ""
        sName = []
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatSumItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # parse the name
            name = row.xpath('td[2]/a/text()').extract()
            sName = name[0].split(' ',1)
            loader.add_value('first_name', sName[0])
            loader.add_value('last_name', sName[1])
            
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
            
            # collect several other data points
            loader.add_xpath('position', './/td[4]/text()')
            loader.add_xpath('games_played', './/td[5]/text()')
            loader.add_xpath('goals', './/td[6]/text()')
            loader.add_xpath('assists', './/td[7]/text()')
            loader.add_xpath('points', './/td[8]/text()')
            loader.add_xpath('plus_minus', './/td[9]/text()')
            loader.add_xpath('penalty_minutes', './/td[10]/text()')
            loader.add_xpath('pp_goals', './/td[11]/text()')
            loader.add_xpath('pp_points', './/td[12]/text()')
            loader.add_xpath('sh_goals', './/td[13]/text()')
            loader.add_xpath('sh_points', './/td[14]/text()')
            loader.add_xpath('gw_goals', './/td[15]/text()')
            
            # NHL stopped tracking tying goals in 2005, forcing an adjustment
            if shootout:
                loader.add_xpath('ot_goals', './/td[16]/text()')
                loader.add_xpath('shots', './/td[17]/text()')
                loader.add_xpath('shot_pct', './/td[18]/text()')
            else:
                loader.add_xpath('ot_goals', './/td[17]/text()')
                loader.add_xpath('shots', './/td[18]/text()')
                loader.add_xpath('shot_pct', './/td[19]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider grabs the birth year from the 'Bio' pages.

class SkatBioSpider(CrawlSpider):
    #define class variables
    name = "skatbio"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatBioSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=bios&sort=player.birthCountryAbbrev&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
            
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatBioItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect birth year, convert per NHL CBA
            bDate = row.xpath('td[5]/text()').extract()[0]
            bMonth = bDate[:3]
            bYear = int(bDate[-2:])
            # Players age according to whether or not they where born by June 30th
            if bMonth in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']:
                bYear = bYear+1
            bYear = str(bYear+1900)
            loader.add_value('birth_year', bYear)
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes 'empty net goal' stats from 'goals' pages.

class SkatEngSpider(CrawlSpider):
    #define class variables
    name = "skateng"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatEngSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=goals&sort=goals&pg=1" % season]

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
            loader = ItemLoader(SkatEngItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            if shootout:
                loader.add_xpath('en_goals', './/td[20]/text()')
                loader.add_xpath('ps_goals', './/td[21]/text()')
            else:
                loader.add_xpath('en_goals', './/td[21]/text()')
                loader.add_xpath('ps_goals', './/td[22]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes penalty stats.

class SkatPIMSpider(CrawlSpider):
    name = "skatpim"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatPIMSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=penalties&sort=penaltyMinutes&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
            
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatPIMItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            loader.add_xpath('minors', './/td[7]/text()')
            loader.add_xpath('majors', './/td[8]/text()')
            loader.add_xpath('misconducts', './/td[9]/text()')
            loader.add_xpath('game_misconducts', './/td[10]/text()')
            loader.add_xpath('matches', './/td[11]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes +/- stats.

class SkatPMSpider(CrawlSpider):
    name = "skatpm"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatPMSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=plusMinus&sort=plusMinus&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatPMItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            loader.add_xpath('team_goals_for', './/td[14]/text()')
            loader.add_xpath('team_pp_goals_for', './/td[15]/text()')
            loader.add_xpath('team_goals_against', './/td[16]/text()')
            loader.add_xpath('team_pp_goals_against', './/td[17]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes 'real-time' stats.

class SkatRTSSpider(CrawlSpider):
    name = "skatrts"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatRTSSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=rtssPlayerStats&sort=gamesPlayed&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatRTSItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            loader.add_xpath('hits', './/td[6]/text()')
            loader.add_xpath('blocked_shots', './/td[7]/text()')
            loader.add_xpath('missed_shots', './/td[8]/text()')
            loader.add_xpath('giveaways', './/td[9]/text()')
            loader.add_xpath('takeaways', './/td[10]/text()')
            loader.add_xpath('faceoff_wins', './/td[11]/text()')
            loader.add_xpath('faceoff_losses', './/td[12]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes shootout stats.

class SkatSOSpider(CrawlSpider):
    name = "skatso"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatSOSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=shootouts&sort=goals&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatSOItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            loader.add_xpath('so_shots', './/td[13]/text()')
            loader.add_xpath('so_goals', './/td[14]/text()')
            loader.add_xpath('so_pct', './/td[15]/text()')
            loader.add_xpath('game_deciding_goals', './/td[16]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes overtime stats.

class SkatOTSpider(CrawlSpider):
    name = "skatot"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatOTSpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=scoringLeaders&sort=powerPlayGoals&pg=1" % season]

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
            loader = ItemLoader(SkatOTItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect stats
            if shootout:
                loader.add_xpath('ot_games_played', './/td[16]/text()')
                loader.add_xpath('ot_assists', './/td[18]/text()')
                loader.add_xpath('ot_points', './/td[19]/text()')
            else:
                loader.add_xpath('ot_games_played', './/td[17]/text()')
                loader.add_xpath('ot_assists', './/td[19]/text()')
                loader.add_xpath('ot_points', './/td[20]/text()')
            
            # feed item to pipeline
            yield loader.load_item()

# This spider scrapes Time On Ice stats, converted to seconds.

class SkatTOISpider(CrawlSpider):
    name = "skattoi"
    allowed_domains = ["nhl.com"]
    start_urls = []
    
    # tell parser where to look for links to follow and what to seek
    rules = (Rule(LxmlLinkExtractor(
        allow=('.*&pg=.*'),
        restrict_xpaths=('/html//tfoot[@class="paging"]')),
        callback='parse_item', follow=True
        ),)
    
    # This function allows us to pass an argument to the spider
    # by inserting it into the command line prompt.
    # E.g., scrapy crawl skatsum -a season="1998"
    
    def __init__(self, season="", *args, **kwargs):
        super(SkatTOISpider, self).__init__(*args, **kwargs)
        
        # allows the passing of the command line argument to parse_item method
        self.year = int(season)
        
        # defines the starting URLs procedurally
        self.start_urls = [
            "http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLSASALL"
            "&viewName=timeOnIce&sort=timeOnIce&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        
        # collect xpaths of each player (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        
        # instantiate parsing variables
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatTOIItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # get unique NHL ID number from player's page URL
            num = row.xpath('td[2]/a/@href').extract()
            sNum = num[0][-7:]
            loader.add_value('nhl_num', sNum)
            
            # add season data
            loader.add_value('season', str(self.year))
            
            # collect TOI stats after converting from m,mmm:ss to seconds
            i = 5
            temp = ""
            sTemp = []
            CATEG = ['es_toi', 'sh_toi', 'pp_toi', 'toi']
            while i < 12:
                i += 1
                if i % 2 == 0:
                    temp = row.xpath('td[' + str(i) + ']/text()').extract()[0]
                    sTemp = temp.split(':')
                    sTemp[0] = sTemp[0].replace(',', '')
                    loader.add_value(CATEG[(i-6)/2], str(60*int(sTemp[0]))+sTemp[1])
                else:
                    pass
            
            # feed item to pipeline
            yield loader.load_item()
