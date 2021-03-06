# Scrapy settings for nhlsql project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import datetime as dt

today = dt.datetime.now()

BOT_NAME = 'nhlsql'

SPIDER_MODULES = ['nhlsql.spiders']
NEWSPIDER_MODULE = 'nhlsql.spiders'
LOG_FILE = 'logs/%s.log' % (today.strftime('%y.%m.%d %H:%M:%S'),)

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': os.environ["DB_USER"],
            'password': os.environ["DB_PASS"],
            'database': os.environ["DB_NAME"]}

ITEM_PIPELINES = {'nhlsql.pipelines.PlayerPipeline': 100}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nhlsql (+http://www.yourdomain.com)'
