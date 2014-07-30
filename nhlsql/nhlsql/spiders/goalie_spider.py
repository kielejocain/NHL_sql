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
        name = ""
        sName = []
        num = 0
        
        # loop through players
        for row in rows:
            loader = ItemLoader(SkatSumItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()
            
            # parse the name
            name = cell.xpath('td[2]/a/text()').extract()
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
            
            # collect several other stats
            loader.add_value('position', 'G')
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

# This spider scrapes penalty shot stats.

class GoalPSSpider(CrawlSpider):
    name = "goalps"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(SgmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    def __init__(self, season, *args, **kwargs):
        super(GoalPSSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=penaltyShot&sort=penaltyShotsAgainst&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        cells = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        items = []
        num = 0
        for cell in cells:
            item = GoalPSItem()
            num = cell.xpath('td[2]/a/@href').extract()
            sNum = int(num[0][-7:])
            item['nhl_num'] = sNum
            item['ps_attempts'] = int(cell.xpath('td[6]/text()').extract()[0])
            item['ps_goals_against'] = int(cell.xpath('td[7]/text()').extract()[0])
            item['ps_saves'] = int(cell.xpath('td[8]/text()').extract()[0])
            items.append(item)
        return items

# This spider scrapes shootout stats.

class GoalSOSpider(CrawlSpider):
    name = "goalso"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(SgmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    def __init__(self, season, *args, **kwargs):
        super(GoalSOSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=shootouts&sort=shootoutGamesWon&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        cells = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        items = []
        num = 0
        for cell in cells:
            item = GoalSOItem()
            num = cell.xpath('td[2]/a/@href').extract()
            sNum = int(num[0][-7:])
            item['nhl_num'] = sNum
            item['so_wins'] = int(cell.xpath('td[14]/text()').extract()[0])
            item['so_losses'] = int(cell.xpath('td[15]/text()').extract()[0])
            item['so_shots_against'] = int(cell.xpath('td[16]/text()').extract()[0])
            item['so_goals_against'] = int(cell.xpath('td[17]/text()').extract()[0])
            items.append(item)
        return items

# This spider scrapes special teams stats.

class GoalSTSpider(CrawlSpider):
    name = "goalst"
    allowed_domains = ["nhl.com"]
    start_urls = []

    rules = (Rule(SgmlLinkExtractor(
                                    allow=('.*&pg=.*'),
                                    restrict_xpaths=('/html//tfoot[@class="paging"]')
                                    ),
                  callback='parse_item', follow=True
                  ),)
    
    def __init__(self, season, *args, **kwargs):
        super(GoalSTSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.nhl.com/ice/playerstats.htm?fetchKey=%s2ALLGAGALL"
                  "&viewName=specialTeamSaves&sort=evenStrengthSaves&pg=1" % season]

    def parse_item(self, response):
        sel = Selector(response)
        cells = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')
        items = []
        num = 0
        for cell in cells:
            item = GoalSTItem()
            num = cell.xpath('td[2]/a/@href').extract()
            sNum = int(num[0][-7:])
            item['nhl_num'] = sNum
            i = 5
            CATEG = [
                     'es_shots_against', 'es_goals_against', 'es_saves', 'es_save_pct',
                     'pp_shots_against', 'pp_goals_against', 'pp_saves', 'pp_save_pct',
                     'sh_shots_against', 'sh_goals_against', 'sh_saves', 'sh_save_pct'
                     ]
            while i < 17:
                i += 1
                if i % 4 == 1:
                    try:
                        item[CATEG[i-6]] = float(cell.xpath('td[' + str(i) + ']/text()').extract()[0])
                    except IndexError:
                        item[CATEG[i-6]] = 0.0
                else:
                    item[CATEG[i-6]] = int(cell.xpath('td[' + str(i) + ']/text()').extract()[0])
            items.append(item)
        return items