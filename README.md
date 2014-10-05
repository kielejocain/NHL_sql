NHL_sql
=======

Description
-----------

This repo is a project to cull all season-wide data from the NHL.com statistics pages, importing it into a PostgreSQL database and cleaning it.

Requirements
------------

* [Python 2.7+][1] is required for the use of the framework Scrapy. Python 3+ is not supported.

* [Scrapy 0.24.2][2] is used, which has several dependancies, including lxml and OpenSSL.

* [Sqlalchemy][3] is another required Python module.

* This script is known to work with [PostgreSQL][4] versions 9.1.4 and 9.3.4, and with a small amount of tweaking (likely in the settings and .SQL files) can likely be made to work with several other SQL databases as well.

* One needs to be able to run bash scripts.  They were written to work in Ubuntu; I haven't tested their ability to function in Windows with win-bash or the terminal included with Windows' or OS X's Git install.

Sequence to obtain data
-----------------------

1. Install dependancies

2. Set up file structure (remove `-TEMPLATE` from `nhlsql/settings/py` and `*_clean.sh`), add `logs` directory in parent directory (with `scrapy.cfg`)

3. Create database, enter details into former `-TEMPLATE` files (e.g., `[--psql username--]` is usually `postgres` by default)

4. Connect to that database with a terminal or GUI (like pgAdmin)

5. In a (distinct) terminal run `skater_crawl.sh` and `goalie_crawl.sh`.  This will obtain all the data over several minutes, storing it in disparate tables representing several different classes of NHL.com statistics pages.

6. Run `skat_clean.sh` and `goal_clean.sh` in your SQL terminal/GUI, which will clean and normalize you data as described below.

Schema
------

Though it may be generous to call it a 'schema,' what you'll find of value when the process is finished are two tables of player biography data titled `skaters` and `goalies`, along with the respective collections of seasonwide statistics in the tables `skaterstats` and `goaliestats`.  The biography tables are keyed by the NHL's unique 7-digit identifying numbers for the players in the `nhl_num` column.  As such, a query looking for all 50+ goal scorers in the last 10 years might look like:

`SELECT last_name, first_name, season, goals`

`FROM skaters, skaterstats`

`WHERE skaters.nhl_num = skaterstats.nhl_num AND season > 2003 AND goals >= 50`

`ORDER BY goals DESC;`

Known Issues
------------

* None as of last commit.

Acknowledgements
----------------

The base of the Scrapy code came from the fantastic tutorials at [newcoder.io][5], which I have heavily editted and brought in line with the current (0.24.4 as of this creation) version of Scrapy.

[1]: https://www.python.org/download/   "Download Python"
[2]: http://doc.scrapy.org/en/latest/intro/install.html "Scrapy Installation Guide"
[3]: http://www.sqlalchemy.org/download.html "Download - SQLAlchemy"
[4]: http://www.postgresql.org/download/ "PostgreSQL: Downloads"
[5]: http://newcoder.io/scrape/ "New Coder - Web Scraper"
