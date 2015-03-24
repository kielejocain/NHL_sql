from sqlalchemy.orm import sessionmaker

from models import *

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PlayerPipeline(object):
    """pipeline for storing skater summary items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates skater summary table.
        """
        engine = db_connect()
        create_skater_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save players in the database.

        This method is called for every item in the pipeline component.

        """
        session = self.Session()
        whois = spider.name
        if whois == 'skatsum':
            player = SkaterSum(**item)
        elif whois == 'skatbio':
            player = SkaterBio(**item)
        elif whois == 'skateng':
            player = SkaterEng(**item)
        elif whois == 'skatpim':
            player = SkaterPIM(**item)
        elif whois == 'skatpm':
            player = SkaterPM(**item)
        elif whois == 'skatrts':
            player = SkaterRTS(**item)
        elif whois == 'skatso':
            player = SkaterSO(**item)
        elif whois == 'skatot':
            player = SkaterOT(**item)
        elif whois == 'skattoi':
            player = SkaterTOI(**item)
        elif whois == 'goalsum':
            player = GoalieSum(**item)
        elif whois == 'goalbio':
            player = GoalieBio(**item)
        elif whois == 'goalps':
            player = GoaliePS(**item)
        elif whois == 'goalso':
            player = GoalieSO(**item)
        elif whois == 'goalst':
            player = GoalieST(**item)
        elif whois == 'standings':
            player = StandingsModel(**item)

        try:
            session.add(player)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    
        return item
