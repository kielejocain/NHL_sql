NHL_sql
=======

Description
-----------

This repo is a project to cull all season-wide data from the NHL.com statistics pages, importing it into a PostgreSQL database and cleaning it.

Requirements
------------

As I'm relatively new to Unix-based environments, I'll simply preface this install sequence with the fact that I'm running Ubuntu (this works on both 12.04 and 14.04).

* [Python 2.7+][1] is required for the use of the framework Scrapy. Python 3+ is not supported.  `pip` is also assumed for package installation.

```
sudo apt-get update
sudo apt-get python-dev
sudo apt-get install python-pip
```

* I would highly recommend using a python virtual environment for this project, as there are numerous required modules that may not play nice with others.  There are several quality guides out there for installing `virtualenv` (and `virtualenvwrapper`, if you like).

* This script is known to work with [PostgreSQL][4] versions 9.1.4 and 9.3.5, and with a small amount of tweaking (likely in the settings and .SQL files) can likely be made to work with several other SQL databases as well.

* You'll also need to install libraries and headers for C development; in Ubuntu, this amounts to

```
sudo apt-get install libffi-dev libxml2-dev libxslt1-dev
sudo apt-get install postgresql-X.Y
sudo apt-get install posgresql-server-dev-X.Y
```

where `X.Y` is the PostgreSQL version you've installed (*e.g.*, `9.3`).

* [Scrapy 0.24.4][2] is the version in which this code is known to work.  This module requires SEVERAL other pieces to install, which the `pip` script will happily do for you if your machine has the requisite libraries. If you're not in a virtual environment, you may need `sudo`.

```
pip install scrapy==0.24.4
```

* The python module [Sqlalchemy][3] will require the Python development headers, as well as the python module `psycopg2`.  Finally, the `Twisted` module complains unless you install the `service_identity` module to go with it.

```
sudo apt-get install python-dev
pip install psycopg2
pip install sqlalchemy
pip install service_identity
```

* Alternatively, you can install all python modules (after all header files are installed) by the following command.  You'll still need to install all the libraries and headers above with `apt`.

```
pip install -r requirements.txt
```

* One needs to be able to run bash scripts.  They were written to work in Ubuntu; I haven't tested their ability to function in any other environment, but they are exceedingly basic and should be easily rewritten at worst.

Sequence to obtain data
-----------------------

1. Install dependencies

2. Add `logs` directory in parent directory (with `scrapy.cfg`)

3. Create database, save details into the environment variables $DB_NAME (name of the database), $DB_USER (user of the database in postgres), and $DB_PASS (password for the user $DB_USER)

4. Run `init_scrape.sh`.  These will obtain all the data over several minutes, storing it in disparate tables representing several different classes of NHL.com statistics pages.  It will then run the `*_clean.sql` and `*_join.sql` commands in psql to fix the NHL's silly way of handling shootout statistics, and to join all the various tables into one coherent one for players and goalies.

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
