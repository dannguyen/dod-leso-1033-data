# SQL stuff 

just random sql doodles


## Which items in old report don't exist in new report?

```sql
WITH pd AS (
    SELECT * FROM compiled_agency 
    WHERE station_name = 'AUSTIN POLICE DEPT'
        AND state = 'TX'
    ORDER BY file_date ASC),
    current AS (
        SELECT * FROM pd
        WHERE file_date = '2020-03-31'
    ), old AS (
        SELECT * FROM pd
        WHERE file_date = '2016-04-04'
    )
SELECT o.*, c.*
FROM old AS o
LEFT JOIN current AS c
    USING(item_name)
WHERE c.item_name IS NULL
```


## trying to figure out if time element in ship date is just an artifact

TODO: count within agency

```sql
with shipdates AS (SELECT ship_date, count(1) as n
FROM compiled_agency
GROUP BY ship_date
ORDER BY ship_date ASC)

SELECT 
    SUBSTR(ship_date, 1, 10) AS day
    , COUNT(1) AS j, SUM(n) AS z
FROM shipdates
GROUP BY day
ORDER BY j DESC 
```
