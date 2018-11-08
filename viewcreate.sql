--main view
CREATE view log_article_author AS
SELECT log.id AS logId, log.time AS logTime, log.status AS logStatus,
    log.path AS logPath, articles.title AS articleTitle, authors.name AS authorName 
FROM log LEFT JOIN articles ON log.path = concat('/article/',articles.slug) 
LEFT JOIN authors ON articles.author = authors.id;

--error logs view
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

SELECT articleTitle, count(articleTitle) AS articleViews 
FROM log_article_author
WHERE articleTitle IS NOT NULL
GROUP BY articleTitle
ORDER BY articleViews DESC
LIMIT 3;

SELECT authorName, count(authorName) AS authorViews
FROM log_article_author
WHERE authorName IS NOT NULL
GROUP BY authorName
ORDER BY authorViews DESC;

SELECT errDate::DATE, errPct
FROM error_pct_log
WHERE errPct >0.01;