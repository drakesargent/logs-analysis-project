# Logs Analysis Project
## Description
This program connects to a database, performs queries, and prints results with headings for each query. The queries are run at launch of the application script without user intervention and exits upon completion.
## Pre-Run Notice
The application assumes that two views have been created on the postgrsql database. The first view joins the log, articles, and authors tables. The second view, based off of the first creates an error specific log view.
**Code for view 1:**
'''sql
CREATE view log_article_author AS
SELECT log.id AS logId, log.time AS logTime, log.status AS logStatus,
    log.path AS logPath, articles.title AS articleTitle, authors.name AS authorName 
FROM log LEFT JOIN articles ON log.path = concat('/article/',articles.slug) 
LEFT JOIN authors ON articles.author = authors.id;
'''
**Code for view 2:**
'''sql
CREATE view error_pct_log AS
SELECT aLogs.logDay AS errDate, 
CAST(count(eLogs.logStatus) AS DOUBLE PRECISION)/CAST(count(aLogs.logStatus) AS DOUBLE PRECISION) AS errPct
FROM
(Select to_char(logTime, 'YYYY-MM-DD') AS logDay, logStatus, logId 
    From log_article_author) AS aLogs
LEFT JOIN
(SELECT to_char(logTime, 'YYYY-MM-DD') AS logDay, logStatus, logId 
    FROM log_article_author
    WHERE logStatus LIKE '%4__%') AS eLogs
ON aLogs.logID = eLogs.logId
GROUP BY aLogs.logDay;
'''
##Instructions##
To run the application script, on the command prompt type:
'''cmd
python3 print_reports.py
'''
Then press enter or return.
##Notes##
The queries take a few seconds each to run. As a result the output to the screen may appear stalled or delayed. Future versions will make use of materialized views to speed up queries.
##Contact##
Any questions or feedback please email me [kennethrsargent@gmail.com](mailto:kennethrsargent@gmail.com?Subject=Print%20Reports%20Question).