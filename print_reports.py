#!/usr/bin/env python3

import psycopg2
import datetime

# constant for DB name
DATABASE_NAME = "news"

# queries
errorQuery = """
SELECT errDate::DATE, errPct
FROM error_pct_log
WHERE errPct >0.01;
"""

popularViewQuery = """
SELECT articleTitle, count(articleTitle) AS articleViews
FROM log_article_author
WHERE articleTitle IS NOT NULL
GROUP BY articleTitle
ORDER BY articleViews DESC
LIMIT 3;
"""

authorViewQuery = """
SELECT authorName, count(authorName) AS authorViews
FROM log_article_author
WHERE authorName IS NOT NULL
GROUP BY authorName
ORDER BY authorViews DESC;
"""


# function to return query data
def queryData(db, query):
    conn = psycopg2.connect(database=db)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


# Report 1: 3 most popular articles
popularArticles = queryData(DATABASE_NAME, popularViewQuery)
print("Top 3 articles:")
for article in popularArticles:
    print('"{}" -- {}'.format(article[0], article[1]))

# Report 2: number of views by author
authorViews = queryData(DATABASE_NAME, authorViewQuery)
print("\nNumber of views by author:")
for author in authorViews:
    print("{} -- {} views".format(author[0], author[1]))

# Report 3: dates of errors > than 1%
errorReport = queryData(DATABASE_NAME, errorQuery)
print("\nDays with errors >1%:")
for error in errorReport:
    print("{} -- {:.2%} errors".format(error[0].strftime("%B %d, %Y"),
                                       error[1]))
