#!/bin/bash

season="2015"
user="postgres"

scrapy crawl skatsum -a season="${season}"
echo "skatsum${season}"
scrapy crawl skatbio -a season="${season}"
echo "skatbio${season}"
scrapy crawl skateng -a season="${season}"
echo "skateng${season}"
scrapy crawl skatpim -a season="${season}"
echo "skatpim${season}"
scrapy crawl skatpm -a season="${season}"
echo "skatpm${season}"
scrapy crawl skatrts -a season="${season}"
echo "skatrts${season}"
scrapy crawl skatso -a season="${season}"
echo "skatso${season}"
scrapy crawl skatot -a season="${season}"
echo "skatot${season}"
scrapy crawl skattoi -a season="${season}"
echo "skattoi${season}"

scrapy crawl goalsum -a season="${season}"
echo "goalsum${season}"
scrapy crawl goalbio -a season="${season}"
echo "goalbio${season}"
scrapy crawl goalps -a season="${season}"
echo "goalps${season}"
scrapy crawl goalso -a season="${season}"
echo "goalso${season}"
scrapy crawl goalst -a season="${season}"
echo "goalst${season}"

sudo -u ${user} psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/skat_clean.sql
sudo -u ${user} psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/goal_clean.sql
sudo -u ${user} psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/curr_skat_join.sql
sudo -u ${user} psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/curr_goal_join.sql

exit