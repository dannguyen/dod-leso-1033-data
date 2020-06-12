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


## Find each unique state-agency, with total orders, orders in latest file, orders in oldest file, total reports, first date, and last date

```sql
WITH usums AS (
        SELECT state
            , station_name
            , file_date
            , COUNT(1) as record_count
        FROM compiled_agency
        GROUP BY state, station_name, file_date
        ORDER BY state, station_name, file_date
    )
    , ua AS (
    SELECT state
        , station_name
        , COUNT(1) AS file_count
        , SUM(order_count) AS order_count
        , MIN(file_date) AS oldest_date
        , MAX(file_date) AS latest_date
    FROM usums
    GROUP BY state, station_name
)
SELECT * 
FROM ua;


```



## In each dated file, find the records for which there are repeat orders for the same item/quantity
