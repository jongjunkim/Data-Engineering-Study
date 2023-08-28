## How to copy SQL table to Amazon Redshift

* Create table in Redshift(OLAP, DataWarehouse)
```SQL
CREATE TABLE (schema).nps (
 id INT NOT NULL primary key,
 created_at timestamp,
 score smallint
);
```

* SqlToS3Operator
  * MySQL SQL -> S3
* S3ToRedshiftOperator
  * S3 -> Redshift Table
 
```Python
dag = DAG(
    dag_id = 'MySQL_to_Redshift',
    start_date = datetime(2022,8,24), 
    schedule = '0 9 * * *',  
    max_active_runs = 1,
    catchup = False,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

schema = "rkdlem196"
table = "nps"
s3_bucket = "grepp-data-engineering"
s3_key = schema + "-" + table

mysql_to_s3_nps = SqlToS3Operator(
    task_id = 'mysql_to_s3_nps',
    query = "SELECT * FROM prod.nps",
    s3_bucket = s3_bucket,
    s3_key = s3_key,
    sql_conn_id = "mysql_conn_id",
    aws_conn_id = "aws_conn_id",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": False},    
    dag = dag
)

s3_to_redshift_nps = S3ToRedshiftOperator(
    task_id = 's3_to_redshift_nps',
    s3_bucket = s3_bucket,
    s3_key = s3_key,
    schema = schema,
    table = table,
    copy_options=['csv'],
    method = 'REPLACE', #"Replace" in case of Full Refresh and "Upsert" in case of upsert(update and insert)
    redshift_conn_id = "redshift_dev_db",
    aws_conn_id = "aws_conn_id",
    dag = dag
)

mysql_to_s3_nps >> s3_to_redshift_nps
```

* MySql incremental Update
```Python
dag = DAG(
    dag_id = 'MySQL_to_Redshift_v2',
    start_date = datetime(2023,1,1), 
    #excution_date = datetime(2023,1,1),
    #end_date = datetime(2023,6,10),
    schedule = '0 9 * * *', 
    max_active_runs = 1,
    catchup = True,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

schema = "rkdlem196"
table = "nps"
s3_bucket = "grepp-data-engineering"
s3_key = schema + "-" + table       # s3_key = schema + "/" + table

sql = "SELECT * FROM prod.nps WHERE DATE(created_at) = DATE('{{ execution_date }}')" #incremental update
print(sql)
mysql_to_s3_nps = SqlToS3Operator(
    task_id = 'mysql_to_s3_nps',
    query = sql,
    s3_bucket = s3_bucket,
    s3_key = s3_key,
    sql_conn_id = "mysql_conn_id",
    aws_conn_id = "aws_conn_id",
    verify = False,
    replace = True,
    pd_kwargs={"index": False, "header": False},    
    dag = dag
)

s3_to_redshift_nps = S3ToRedshiftOperator(
    task_id = 's3_to_redshift_nps',
    s3_bucket = s3_bucket,
    s3_key = s3_key,
    schema = schema,
    table = table,
    copy_options=['csv'],
    redshift_conn_id = "redshift_dev_db",
    aws_conn_id = "aws_conn_id",    
    method = "UPSERT",
    upsert_keys = ["id"],
    dag = dag
)

mysql_to_s3_nps >> s3_to_redshift_nps
```
* ## Creating Summary Table
```Python
def execSQL(**context):

    schema = context['params']['schema'] 
    table = context['params']['table']
    select_sql = context['params']['sql']

    logging.info(schema)
    logging.info(table)
    logging.info(select_sql)

    cur = get_Redshift_connection()

    sql = f"""DROP TABLE IF EXISTS {schema}.temp_{table};CREATE TABLE {schema}.temp_{table} AS """
    sql += select_sql
    cur.execute(sql)

    cur.execute(f"""SELECT COUNT(1) FROM {schema}.temp_{table}""")
    count = cur.fetchone()[0]
    if count == 0:
        raise ValueError(f"{schema}.{table} didn't have any record")

    try:
        sql = f"""DROP TABLE IF EXISTS {schema}.{table};ALTER TABLE {schema}.temp_{table} RENAME to {table};"""
        sql += "COMMIT;"
        logging.info(sql)
        cur.execute(sql)
    except Exception as e:
        cur.execute("ROLLBACK")
        logging.error('Failed to sql. Completed ROLLBACK!')
        raise AirflowException("")


dag = DAG(
    dag_id = "Build_Summary",
    start_date = datetime(2021,12,10),
    schedule = '@once',
    catchup = False
)

execsql = PythonOperator(
    task_id = 'mau_summary',
    python_callable = execSQL,
    params = {
        'schema' : 'rkdlem196',
        'table': 'mau_summary',
        'sql' : """SELECT 
  TO_CHAR(A.ts, 'YYYY-MM') AS month,
  COUNT(DISTINCT B.userid) AS mau
FROM raw_data.session_timestamp A
JOIN raw_data.user_session_channel B ON A.sessionid = B.sessionid
GROUP BY 1 
;"""
    },
    dag = dag
)
```
