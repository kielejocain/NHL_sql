#!/bin/bash

for season in 2006 2007 2008 2009 2010 2011 2012 2013 2014
do
sudo -u postgres psql -d nhltest -v season=${season} -f skat_clean.sql
done
sudo -u postgres psql -d nhltest -f skater_join.sql
exit
