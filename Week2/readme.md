 ## SQL

* ### SELECT

```SQL
SELECT userId, sessionId, channel
FROM raw_data.user_session_channel;

SELECT *
FROM raw_data.user_session_channel
LIMIT 10;

SELECT COUNT(1)
FROM raw_data.user_session_channel;
```

* ### Where

* #### IN
  
WHERE channel in (‘Google’, ‘Youtube’)

WHERE channel = ‘Google’ OR channel = ‘Youtube’

* #### NOT IN.
LIKE and ILIKE

LIKE is a case sensitive string match. ILIKE is a case-insensitive string match

WHERE channel LIKE ‘G%’ -> ‘G*’

WHERE channel LIKE ‘%o%’ -> ‘*o*’ 

NOT LIKE or NOT ILIKE

* BETWEEN
Used for date range matching

```SQL
SELECT COUNT(1)
FROM raw_data.user_session_channel
WHERE channel in 
('Google','Facebook');
```

* ### STRING Functions
* LEFT(str, N)
* REPLACE(str, exp1, exp2)
* UPPER(str)
* LOWER(str)
* LEN(str)
* LPAD, RPAD
* SUBSTRING

* ### ORDER BY
* Default ordering is ascending
* Descending requires "DESC"
* Ordering by multiple columns

* ### JOIN
![6 types JOIN](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/SQL-JOINS-Example-0.jpg)



