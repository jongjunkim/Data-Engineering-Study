## Airflow Deepdive 2

* ## Notice when you code in dags folder
  * Airflow periodically scans the "dags" folder.
  * During this process, the main functions of all the files containing DAG modules are executed. In this situation, unintendedly, even test code under development   
    could be executed.
  * Solution: put .airflowignore in dags folder

* ## Create Open Weathermap API (DAG created by API)

```SQL
CREATE TABLE jongjun.weather_forecast (
 date date primary key,
 temp float,
 min_temp float,
 max_temp float,
 created_date timestamp default GETDATE()
);
```

* ## Primary Key Uniqueness
  * Prevent to have duplicated primary key in relational database system
  * However, a Data Warehouse based on a big database doesn't keep Primary Key

*  ## Solution
*  ROW_NUMBER!!!!
```SQL
*  ROW_NUMBER() OVER (partition by date
order by created_date DESC) seq
```



