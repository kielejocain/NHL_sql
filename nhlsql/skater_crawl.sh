#!/bin/bash

for year in 98 99 00 01 02 03 04 06 07 08 09 10 11 12 13 14
do
echo "file = $f"
sudo -u postgres psql -d nhldata -c "copy skaters from '$f' csv header delimiter as ',';"
done

exit
