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
![image](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/uniqueness.PNG)

* if you want to order by date and recently created_date
* Add one column named "seq", so that we can easily see the recent data from top to bottom

* ## Steps to keep Primary Key Uniqueness

1. Create a temporary table named "t" and populate it with the contents of the "jongjun.weather_forecast" table.
  * copies the data from the original table to a temporary table.
    
2. The DAG (Directed Acyclic Graph) adds records to the temporary table (staging table).
  * it's noted that duplicate data could potentially be inserted.
3. Delete records from the "keeyong.weather_forecast" table.
4. Create a new table without duplicated data
   * ex ) Use Row_number()

```Python
@task
def etl(schema, table):
    api_key = Variable.get("open_weather_api_key")
    # Latitude and Longitude for Seoul
    lat = 37.5665
    lon = 126.9780

    # https://openweathermap.org/api/one-call-api
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&exclude=current,minutely,hourly,alerts"
    response = requests.get(url)
    data = json.loads(response.text)
    """
    {'dt': 1622948400, 'sunrise': 1622923873, 'sunset': 1622976631, 'moonrise': 1622915520, 'moonset': 1622962620, 'moon_phase': 0.87, 'temp': {'day': 26.59, 'min': 15.67, 'max': 28.11, 'night': 22.68, 'eve': 26.29, 'morn': 15.67}, 'feels_like': {'day': 26.59, 'night': 22.2, 'eve': 26.29, 'morn': 15.36}, 'pressure': 1003, 'humidity': 30, 'dew_point': 7.56, 'wind_speed': 4.05, 'wind_deg': 250, 'wind_gust': 9.2, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': 44, 'pop': 0, 'uvi': 3}
    """
    ret = []
    for d in data["daily"]:
        day = datetime.fromtimestamp(d["dt"]).strftime('%Y-%m-%d')
        ret.append("('{}',{},{},{})".format(day, d["temp"]["day"], d["temp"]["min"], d["temp"]["max"]))

    cur = get_Redshift_connection()
    drop_recreate_sql = f"""DROP TABLE IF EXISTS {schema}.{table};
CREATE TABLE {schema}.{table} (
    date date,
    temp float,
    min_temp float,
    max_temp float,
    created_date timestamp default GETDATE()
);
"""
    insert_sql = f"""INSERT INTO {schema}.{table} VALUES """ + ",".join(ret)
    logging.info(drop_recreate_sql)
    logging.info(insert_sql)
    try:
        cur.execute(drop_recreate_sql)
        cur.execute(insert_sql)
        cur.execute("Commit;")
    except Exception as e:
        cur.execute("Rollback;")
        raise

with DAG(
    dag_id = 'Weather_to_Redshift',
    start_date = datetime(2023,5,30),
    schedule = '0 2 * * *',  
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
) as dag:

    etl("jongjun", "weather_forecast")

```

* ## Backfill
* The term for this situation is "data pipeline reprocessing."
* It refers to the act of re-executing a failed data pipeline or re-reading data that needs to be ingested again due to issues with either the pipeline itself or the data that was initially processed.
* It is very complicated when the DGA exectues in Incremental update manner
* Airflow is designed well to solve the Backfill issue

* ## To understand start_date and execution date
* ex) Start date: 2020-08-10 02:00:00
* How many times this job is going to be excueted until 2020-08-13 20:00:00
  * 2020-08-10 02:00:00
  * 2020-08-11 02:00:00
  * 2020-08-12 02:00:00
  * 2020-08-13 02:00:00


* `start_date`: The date/time when the DAG should start reading data for the first time, not the actual first execution date of the DAG. The actual first execution date is calculated as `start_date + DAG's execution interval`.

* `execution_date`: The date and time associated with the specific instance of DAG execution. It represents the date and time for which data should be processed.

* `catchup`: A parameter that determines how to handle periods when the DAG is activated (turned on) after its `start_date`. If set to True (default), the DAG will attempt to catch up on missed runs. If set to False, the DAG will ignore runs that occurred before activation.

* `end_date`: This value is generally not required and is only necessary when performing backfilling for a specific date range. The `airflow dags backfill -s … -e 






* Reference:
 * https://school.programmers.co.kr/app/courses/17123/curriculum
