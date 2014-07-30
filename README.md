NHL_sql
=======

Description
-----------

This repo is a project to cull all season-wide data from the NHL.com statistics pages, importing it into a PostreSQL database and cleaning it.

Requirements
------------

* Python 2.7+ is required for the use of the framework Scrapy. Python 3+ is not supported.

* Scrapy 0.24.2 is used, which has several dependancies, including lxml and OpenSSL.

* Sqlalchemy is another required Python module.

Known Issues
------------

* At present, some NHL pages break out a player's statistics over several lines, one for each team.  In particular this occurs on the goalie shootout pages.
