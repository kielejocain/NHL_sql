#!/bin/bash

for year in 98 99 00 01 02 03 04 06 07 08 09 10 11 12 13 14
do
if [ ${year} -gt 50 ]
    then
        season="19${year}"
    else
        season="20${year}"
fi
scrapy crawl goalsum -a season="${season}"
echo "goalsum${year}"
scrapy crawl goalbio -a season="${season}"
echo "goalbio${year}"
scrapy crawl goalps -a season="${season}"
echo "goalps${year}"
scrapy crawl goalso -a season="${season}"
echo "goalso${year}"
scrapy crawl goalst -a season="${season}"
echo "goalst${year}"

done

exit
