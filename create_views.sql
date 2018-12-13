--Run: psql -d news -f create_views.sql--
--    to create the views below for the queries in print_reports.py--
--View for Article/Author queries--
CREATE view article_author AS
SELECT
    log.path AS logPath,
    articles.title AS articleTitle,
    authors.name AS authorName
FROM log
RIGHT JOIN articles
ON log.path = concat('/article/',articles.slug)
LEFT JOIN authors
ON articles.author = authors.id;

--View for Error Pct query--
CREATE view error_pct_log AS
SELECT aLogs.logDay AS errDate,
(eLogs.total_errors::DOUBLE PRECISION/alogs.total_hits::DOUBLE PRECISION) AS errPCT
FROM (
  SELECT time::date AS logDay, count(*) AS total_hits
  FROM log
  GROUP BY logDay
) AS aLogs
LEFT JOIN
(SELECT time::date AS logDay, count(*) as total_errors
    FROM log
    WHERE status LIKE '%4__%'
    GROUP BY logDay
  ) AS eLogs
ON aLogs.logDay = eLogs.logDay;