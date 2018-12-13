# Logs Analysis Project
## Description
This program connects to a PostgreSQL database, performs queries, 
and prints results with headings for each query. The queries are run at launch 
of the application script without user intervention and exits upon completion.

The *news* database is for a fictional news website. It contains 3 tables:
articles, authors, and log. Authors is related to articles through a primary
 key - foreign key using the id from the author table. Log is related to
  articles by log.path and concatenating '/article/' and article.slug.

This program runs queries on the data in the news database to answer the
questions:
* What are the top 3 most read articles of all time?
* Who are the top 3 authors by viewed articles?
* On what days were requests to the site errors more than 1%?

## Requirements
### Environment
#### Provided
I used a [Vagrant](https://www.vagrantup.com/) machine with Oracle [Virtual Box](https://www.virtualbox.org/) 
for virtualization. The Vagrantfile included in the repository will set up the 
required environment and initialize the news database. To do this, open your 
preferred commandline utility to the directory where you cloned this repository 
and run: 
```
vagrant up
```

This process will take some time to finalize.

The database schema and data for the news database will have to be loaded from 
the supplied script in the archive named *newsdata.zip*. Extract the contents 
to the same directory as the other repository files.
Once completed, to connect to the environment run: 
```
vagrant ssh
```

From the vagrant shell, navigate to the directory containing the files from the 
repository. To populate the news database, from the command line 
run: 
```
psql -d news -f newsdata.sql
```

Once completed, to create the required views for this application, run the 
following from the command line: 
```
psql -d news -f create_views.sql
```

#### Custom
Should you choose to use your own environment, you will need to install and 
configure the following:

[Python version 3](https://www.python.org/downloads/)

[psycopg2 version 2.7](http://initd.org/psycopg/download/)

[PostgreSQL](https://www.postgresql.org/download/)

##Instructions

To run the application, on the command line type:
```cmd
python print_reports.py
```
Then press enter or return.

**Contact:**

Any questions or feedback please email me [kennethrsargent@gmail.com](mailto:kennethrsargent@gmail.com?Subject=Print%20Reports%20Question).
