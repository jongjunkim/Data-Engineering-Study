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
![airflow_DAG](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/running%20dag.PNG)
