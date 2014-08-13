#!/bin/bash

for year in 98 99 00 01 02 03 04 06 07 08 09 10 11 12 13 14
do
if [ ${year} -gt 50 ]
    then
        season="19${year}"
    else
        season="20${year}"
fi
scrapy crawl skatsum -a season="${season}"
echo "skatsum${year}"
scrapy crawl skatbio -a season="${season}"
echo "skatbio${year}"
scrapy crawl skateng -a season="${season}"
echo "skateng${year}"
scrapy crawl skatpim -a season="${season}"
echo "skatpim${year}"
scrapy crawl skatpm -a season="${season}"
echo "skatpm${year}"
scrapy crawl skatrts -a season="${season}"
echo "skatrts${year}"
scrapy crawl skatso -a season="${season}"
echo "skatso${year}"
scrapy crawl skatot -a season="${season}"
echo "skatot${year}"
scrapy crawl skattoi -a season="${season}"
echo "skattoi${year}"

done

exit
