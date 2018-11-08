#!/usr/bin/env python3

import psycopg2
import datetime
# constant for DB name
DATABASE_NAME = "news"

# queries
errorQuery = """
Select ed.errDate::DATE, ed.errPct 
From (Select concat_ws('-',getdate.year, getdate.month, getdate.day) as errDate,
cast(count(statuserr.status) as double precision)/cast(count(getdate.allStatus) as double precision) as errPct
From (Select extract(year from time)as year, extract(month from time) as month, extract(day from time) as day,
status as allStatus, id
From log) as getdate left join (Select status, id from log where status like '%4__%') as statuserr
on getdate.id = statuserr.id
Group by errDate
) as ed
Where ed.errPct > 0.01;
"""

popularViewQuery = """
select title, count(title) numViews from
(select title, author, concat('/article/',slug) as slugPath from articles) as a
join log as l on a.slugPath = l.path
group by title
order by numViews desc
limit 3;
"""

authorViewQuery = """
select authors.name, count(authors.name) numViews from
(select author, concat('/article/',slug) as slugPath from articles
) as artJoin
join log as l on artJoin.slugPath = l.path
join authors on artJoin.author = authors.id
group by name
order by numViews desc;
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
    print("{} -- {:.2%} errors".format(error[0].strftime("%B %d, %Y"), error[1]))
