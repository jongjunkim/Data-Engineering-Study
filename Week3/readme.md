## ETL/Airflow

* ## ETL

* ETL: Extract, Transform, and Load
* Data Pipeline, ETL, Data Workflow, DAG
  * called DAG(Directed Acyclic Graph) in Airflow
* ETL vs ELT
  * ETL:The process of bringing data from an external data warehouse into the internal system.
  * ELT: The process of manipulating internal data within a data warehouse to create new data, often more abstracted and summarized.

* ETL code
```SQL
import requests

def extract(url):
    f = requests.get(url)
    return (f.text)

def transform(text):
    lines = text.strip().split("\n")
    records = []
    for l in lines:
      (name, gender) = l.split(",") # l = "jongjun,M" -> [ 'jongjun', 'M' ]
      records.append([name, gender])
    return records

def load(records):
  cur = get_Redshift_connection()
  for r in records:
        name = r[0]
        gender = r[1]
        print(name, "-", gender)
        sql = f"INSERT INTO jongun.name_gender VALUES ('{name}', '{gender}')"
        print(sql)
        cur.execute(sql)

link = "https:// ~~~"
data = extract(link)
lines = transform(data)
load(lines)
```
* ## Airflow

* Airflow
  * A data pipeline (ETL) framework written in Python.
  * Monitor and schedule data pipeline

* Component of Airflow
  1. Web Server
  2. Scheduler
  3. Worker
  4. Database
  5. Queue

 * Scale up VS Scale out
   * Scale up: Scaling up to higher-performance servers
   * Scale out: Scaling out across multiple servers

* Advantages:
  * Fine-grained control over the data pipeline.
  * Supports various data sources and data warehouses.
  * Easy backfilling process.(Backfill: the process of filling in missing data from the past on the new system that didn't exist before)

 * Disadvantages:
   * Not easy to learn
   * Setting up the development environment can be challenging.
   * Requires complex operational management. Cloud versions are preferred.
    
 * DAG example
```Python
from datetime import datetime, timedelta
from airflow import DAG
default_args = {
    'owner' : 'UserID',
    'start_date' : datetime(2023, 8, 1, hour=0, minute=00),
    'end_date' : datetime(2023, 8, 31, hour=23, minute=00),
    'email' : ['user@gmail.com'],
    'retries' : 1,
    'retry_delay': timedelta(minutes=3),
 }
```
* Full Refresh vs Incremental Update

* Full Refresh: The entire content of the source is read
  * While it might be less efficient, it's simple and easy to maintain. Even if issues arise with the source data, it's straightforward to re-read everything.
  * Not suitable for handling large datasets.

* Incremental Update: more efficient but can be complex and challenging to maintain
  * It usually operates on a daily or hourly basis, reading data from the previous time frame (such as the previous hour or day).
  * Provides efficiency benefits, especially for large datasets, but can become harder to manage as the complexity increases.
  
* Execute Airflow based on Docker
 ![Docker](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/Docker.PNG)
* docker-compose up in cmd
 ![Airflow](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/Airflow.PNG)
![Airflow.UI](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/Airflow_UI.PNG)
