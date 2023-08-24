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
