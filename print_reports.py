#!/usr/bin/env python3

import psycopg2
import datetime

# constant for DB name
DATABASE_NAME = "news"


def dbConnect(DBNAME):
    """
    dbConnect takes a database name as a parameter.
    Creates a connection to a database defined by DBNAME,
    and a cursor for that database.
    args:
    DBNAME - a string that is the name the database to
                    which the function connects

    Returns:
        database, cursor - a tuple.
    """
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    return (conn, cursor)


def executeQuery(query):
    """
    executeQuery takes a SQL query as a parameter.
    Executes query and returns the result as a list of tuples.
    args:
    query - a SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    conn, cursor = dbConnect(DATABASE_NAME)
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def printTopArticles():
    """Prints out the top 3 articles of all time."""

    query = """
    SELECT articleTitle, count(articleTitle) AS articleViews
    FROM article_author
    WHERE articleTitle IS NOT NULL
    GROUP BY articleTitle
    ORDER BY articleViews DESC
    LIMIT 3;
    """
    results = executeQuery(query)
    print("\nTop 3 articles:")
    for title, views in results:
        print('"{}" -- {} views'.format(title, views))


def printTopAuthors():
    """Prints a list of autors ranked by article views."""

    query = """
    SELECT authorName, count(authorName) AS authorViews
    FROM article_author
    WHERE authorName IS NOT NULL
    GROUP BY authorName
    ORDER BY authorViews DESC;
    """
    results = executeQuery(query)
    print("\nNumber of views by author:")
    for author, views in results:
        print("{} -- {} views".format(author, views))


def printErrorDaysOver1Pct():
    """
    Prints out the days where more than 1% of logged
    requests were errors.
    """
    query = """
    SELECT errDate::DATE, errPct
    FROM error_pct_log
    WHERE errPct >0.01;
    """
    results = executeQuery(query)
    print("\nDays with errors >1%:")
    for date, pct in results:
        print("{:%B %d, %Y} -- {:.2%} errors".format(date, pct))


if __name__ == '__main__':

    printTopArticles()
    printTopAuthors()
    printErrorDaysOver1Pct()
