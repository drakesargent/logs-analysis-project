select title, count(title) numViews from
(
select title, author, concat('/article/',slug) as slugPath from articles
) as a
join log as l on a.slugPath = l.path
group by title
order by numViews desc
limit 3;