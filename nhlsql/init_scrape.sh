#!/bin/bash

for season in 1998 1999 2000 2001 2002 2003 2004 2006 2007 2008 2009 2010 2011 2012 2013 2014
do
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
scrapy crawl skatot -a season="${season}"
echo "skatot${season}"
scrapy crawl skattoi -a season="${season}"
echo "skattoi${season}"

scrapy crawl goalsum -a season="${season}"
echo "skatsum${season}"
scrapy crawl goalbio -a season="${season}"
echo "skatbio${season}"
scrapy crawl goalps -a season="${season}"
echo "skateng${season}"
scrapy crawl goalst -a season="${season}"
echo "skatpm${season}"
done

for season in 2006 2007 2008 2009 2010 2011 2012 2013 2014
do
scrapy crawl skatso -a season="${season}"
echo "skatso${season}"
scrapy crawl goalso -a season="${season}"
echo "skatpim${season}"
sudo -u postgres psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/skat_clean.sql
sudo -u postgres psql -d nhltest -v season=${season} -f ~/workspace/NHL_sql/nhlsql/goal_clean.sql
done

sudo -u postgres psql -d nhltest -f skater_join.sql
sudo -u postgres psql -d nhltest -f goalie_join.sql

exit
