#!/bin/bash

sudo -u postgres psql -d nhltest -v season=2015 -f ~/workspace/NHL_sql/nhlsql/skat_clean.sql
sudo -u postgres psql -d nhltest -f ~/workspace/NHL_sql/nhlsql/curr_skat_join.sql
