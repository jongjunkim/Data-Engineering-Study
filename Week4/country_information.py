from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task

from datetime import datetime
from datetime import timedelta

import requests
import logging
import json

def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()

def _create_table(cur, schema, table, drop_first):
    if drop_first:
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS {schema}.{table} (
    country VARCHAR (100),
    population varchar(32),
    area varchar(32)
);""")

@task
def extract(url):
    logging.info(datetime.utcnow())
    f = requests.get(url)
    return (f.text)

@task
def transform(text):
    json_data = json.loads(text)
    extracted_data = []

    for item in json_data:
        common_name = item["name"]["common"]
        official_name = item["name"]["official"]
        population = item["population"]
        area = item["area"]
        extracted_data.append([[common_name, official_name], population, area ])

    return extracted_data

@task
def load(schema, table, records):
    
    logging.info("load started") 
    cur = get_Redshift_connection()

    try:
        cur.execute("BEGIN; ")
        _create_table(cur, schema, table, False)
        cur.execute(f"CREATE TEMP TABLE t AS SELECT * FROM {schema}.{table};")

        #DELTE FROM을 먼저 수행 -> FULL REFRESH하는 형태
        for r in records:
          country_names = ', '.join(r[0])
          country_names = country_names.replace("'", "''")
          population = r[1]
          area = r[2]
          print(country_names, "-", population, "-", area)
          sql = f"INSERT INTO rkdlem196.country_info VALUES ('{country_names}', '{population}', '{area}')"
          print(sql)
          cur.execute(sql)
        
        # Create original table
        _create_table(cur, schema, table, True)
        # Transfer temporary table to original table
        cur.execute(f"INSERT INTO {schema}.{table} SELECT DISTINCT * FROM t;")
        cur.execute("COMMIT;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise
    logging.info("load done")

    

with DAG(
    dag_id='country_information',
    start_date=datetime(2023, 1, 1),  
    schedule='30 6 * * 6',  
    max_active_runs=1,
    catchup=False,
    tags = ['API'],
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
        # 'on_failure_callback': slack.on_failure_callback,
    }
) as dag:

    link = "https://restcountries.com/v3/all"

    data = extract(link)
    item = transform(data)
    load("rkdlem196", "country_info", item)
