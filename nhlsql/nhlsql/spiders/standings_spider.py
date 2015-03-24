# This spider crawls the NHL League Standings page.

from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from nhlsql.standings_items import *

# This spider grabs most classic stats from the 'Summary' pages.


class StandingsSpider(CrawlSpider):
    # define class variables
    name = "standings"
    allowed_domains = ["nhl.com"]
    start_urls = ["http://www.nhl.com/ice/standings.htm?season=20142015&type=LEA"]

    def parse(self, response):
        sel = Selector(response)

        # collect xpaths of each team (row in table)
        rows = sel.xpath('/html//div[@class="contentBlock"]/table/tbody/tr')

        # loop through teams
        for row in rows:
            loader = ItemLoader(StandingsItem(), selector=row)
            loader.default_input_processor = MapCompose()
            loader.default_output_processor = Join()

            # get team identifier
            team = row.xpath('td[2]/a[1]/@rel').extract()
            loader.add_value('team', team)

            # collect several other data points
            loader.add_xpath('division', './/td[3]/text()')
            loader.add_xpath('games_played', './/td[4]/text()')
            loader.add_xpath('wins', './/td[5]/text()')
            loader.add_xpath('losses', './/td[6]/text()')
            loader.add_xpath('ot_losses', './/td[7]/text()')
            loader.add_xpath('points', './/td[8]/text()')
            loader.add_xpath('row', './/td[9]/text()')

            # feed item to pipeline
            yield loader.load_item()