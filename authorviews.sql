select authors.name, count(authors.name) numViews from
(
select author, concat('/article/',slug) as slugPath from articles
) as artJoin
join log as l on artJoin.slugPath = l.path
join authors on artJoin.author = authors.id
group by name
order by numViews desc;