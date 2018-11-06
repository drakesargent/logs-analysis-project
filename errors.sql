-- refactor with better names / etc
Select ed.errDate::DATE, ed.errPct 
From
(
    Select concat_ws('-',getdate.year, getdate.month, getdate.day) as errDate, 
        cast(count(statuserr.status) as double precision)/cast(count(getdate.allStatus) as double precision) as errPct
    From
        (Select extract(year from time)as year, 
                extract(month from time) as month, 
                extract(day from time) as day,
                status as allStatus,
                id
        From log) as getdate left join
        (Select status, id from log where status like '%4__%') as statuserr
    on getdate.id = statuserr.id
    Group by errDate
) as ed
Where ed.errPct > 0.01;