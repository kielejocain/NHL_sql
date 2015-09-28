#!/bin/bash

for season in `seq 2015 -1 2013`;
do
echo "start ${season}"
echo ""
scrapy crawl skatsum -a season="${season}"
echo "skatsum${season}"
scrapy crawl skatpp -a season="${season}"
echo "skatpp${season}"
scrapy crawl skatsh -a season="${season}"
echo "skatsh${season}"
scrapy crawl skatpm -a season="${season}"
echo "skatpm${season}"
scrapy crawl skatbio -a season="${season}"
echo "skatbio${season}"
scrapy crawl skatrts -a season="${season}"
echo "skatrts${season}"
scrapy crawl skatpim -a season="${season}"
echo "skatpim${season}"
scrapy crawl skattoi -a season="${season}"
echo "skattoi${season}"
scrapy crawl skatteam -a season="${season}"
echo "skatteam${season}"

scrapy crawl goalsum -a season="${season}"
echo "goalsum${season}"
scrapy crawl goalbio -a season="${season}"
echo "goalbio${season}"
scrapy crawl goales -a season="${season}"
echo "goales${season}"
scrapy crawl goalpp -a season="${season}"
echo "goalpp${season}"
scrapy crawl goalsh -a season="${season}"
echo "goalsh${season}"
scrapy crawl goalteam -a season="${season}"
echo "goalteam${season}"
echo ""
echo "end ${season}"
echo ""
done

for season in `seq 2015 -1 2013`;
do
scrapy crawl skatso -a season="${season}"
echo "skatso${season}"
scrapy crawl goalso -a season="${season}"
echo "goalso${season}"
done

sudo -u postgres psql -d $DB_NAME -f skater_join.sql
sudo -u postgres psql -d $DB_NAME -f goalie_join.sql

exit
