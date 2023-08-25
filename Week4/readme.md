## Airflow Deepdive

* ## Transaction
* The method of grouping SQL statements that need to be executed atomically, treating them as a single operation, is called "transaction."

* autocommit=True:
  * By default, every SQL statement is immediately committed.
  * To change this behavior, you can use BEGIN;END; or BEGIN;COMMIT (or ROLLBACK) to control transactions.
 ```Python
try:
  cur.execute("BEGIN;")
  cur.execute("DELETE FROM jongjun.name_gender;") 
  cur.execute("INSERT INTO jongjun.name_gender VALUES ('Claire', 'Female');")
  cur.execute("END;")
except (Exception, psycopg2.DatabaseError) as error:
  print(error)
  cur.execute("ROLLBACK;")
finally :
  conn.close()
```   

* autocommit=False:
  * Until I explicitly commit, the changes are only visible to me. They are not visible to others until I commit them
  * By default, SQL statements are not automatically committed.
  * You can use the `.commit()` and `.rollback()` methods of the connection object to decide whether to commit the changes or not.
  * Using try ~ exception and commit is the best practice
```Python
try:
  cur.execute("DELETE FROM jongjun.name_gender;") 
  cur.execute("INSERT INTO jongjun.name_gender VALUES ('Claire', 'Female');")
  conn.commit()  # cur.execute("COMMIT;")
except (Exception, psycopg2.DatabaseError) as error:
  print(error)
  conn.rollback()  # cur.execute("ROLLBACK;")
```

* ## How to run DAG in Airflow
* ### The following Python code is what I am going to execute using Airflow
```Python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    dag_id = 'HelloWorld',
    start_date = datetime(2022,6,14),
    catchup=False,
    tags=['example'],
    schedule = '0 2 * * *')

def print_hello():
    print("hello!")
    return "hello!"

def print_goodbye():
    print("goodbye!")
    return "goodbye!"

print_hello = PythonOperator(
    task_id = 'print_hello',
    #python_callable param points to the function you want to run 
    python_callable = print_hello,
    #dag param points to the DAG that this task is a part of
    dag = dag)

print_goodbye = PythonOperator(
    task_id = 'print_goodbye',
    python_callable = print_goodbye,
    dag = dag)

#Assign the order of the tasks in our DAG
print_hello >> print_goodbye
```
* ## Airflow run
![airflow](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/Airflow%20run.PNG)
* #### Click the Play button on the right side of Hello World
![airflow_DAG](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/running%20dag.PNG)

 ## ETL code in Airflow
 ```Python
def extract(url):
    logging.info("Extract started")
    f = requests.get(url)
    logging.info("Extract done")
    return (f.text)

def transform(text):
    logging.info("Transform started")	
    lines = text.strip().split("\n")[1:] 
    records = []
    for l in lines:
      (name, gender) = l.split(",") # l = "Jongjun,M" -> [ 'Jongjun', 'M' ]
      records.append([name, gender])
    logging.info("Transform ended")
    return records


def load(records):
    logging.info("load started")
    """
    records = [
      [ "Jongjun", "M" ],
      [ "Claire", "F" ],
      ...
    ]
    """
    schema = "Jongjun"
    # Better to use BEGIN and END for SQL transaction
    cur = get_Redshift_connection()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"DELETE FROM {schema}.name_gender;") 
        # Execute Delete First for Full Refresh
        for r in records:
            name = r[0]
            gender = r[1]
            print(name, "-", gender)
            sql = f"INSERT INTO {schema}.name_gender VALUES ('{name}', '{gender}')"
            cur.execute(sql)
        cur.execute("COMMIT;")   # cur.execute("END;") 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK;")   
    logging.info("load done")


def etl():
    link = "https:~~~"
    data = extract(link)
    lines = transform(data)
    load(lines)

dag_second_assignment = DAG(
	dag_id = 'name_gender',
	catchup = False,
	start_date = datetime(2023,4,6)
	schedule = '0 2 * * *')  

task = PythonOperator(
	task_id = 'perform_etl',
	python_callable = etl,
	dag = dag_second_assignment)
```

* DELETE FROM and TRUNCATE:

* Common Point:
  * Both actions involve deleting the contents of a table, which means clearing the table's data.

* Differences:
  * DELETE FROM:
  * You can specify the rows to be deleted using the WHERE clause.
  * Slightly slower compared to TRUNCATE.
  
* TRUNCATE:
  * Deletes the entire table in a single operation and immediately commits the transaction.
  * Should be used only in certain circumstances where the impact is well-understood.
  * Faster in terms of execution speed.




 
* Reference
  * https://programmers.co.kr/learn/courses/12539
  * https://western-sky.tistory.com/160
