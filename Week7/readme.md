## API & Airflow Monitoring

* ## How to check Airflow Health Check
* call /health API
* curl -X GET --user "monitor:MonitorUser1" http://localhost:8080/health
* If the health condition is good, it responses like this
```SQL
 {
 "metadatabase": {
 "status": "healthy"
 },
 "scheduler": {
 "status": "healthy",
 "latest_scheduler_heartbeat": "2022-03-12T06:02:38.067178+00:00"
 }
}
```
* ## Example of using API
* ### Trigger a specfic DAG by API
```SQL
curl -X POST --user "airflow:airflow" -H 'Content-Type: application/json' -d 
'{"execution_date":"2023-05-24T00:00:00Z"}' 
"http://localhost:8080/api/v1/dags/HelloWorld/dagRuns"

{
 "detail": "DAGRun with DAG ID: 'HelloWorld' and DAGRun logical date: '2023-05-24 00:00:00+00:00' 
already exists",
 "status": 409,
 "title": "Conflict",
 "type": 
"https://airflow.apache.org/docs/apache-airflow/2.5.1/stable-rest-api-ref.html#section/Errors/AlreadyExists"
}
```

* ### List all the DAG
```SQL
curl -X GET --user "airflow:airflow" http://localhost:8080/api/v1/dags

{
 "dag_id": "SQL_to_Sheet",
 "default_view": "grid",
 "description": null,
 "file_token": "...",
 "fileloc": "/opt/airflow/dags/SQL_to_Sheet.py",
 "has_import_errors": false,
 "has_task_concurrency_limits": false,
 "is_active": true,
 "is_paused": true,
 "is_subdag": false,
 "last_expired": null,
 "last_parsed_time": "2023-06-18T05:21:34.266335+00:00",
 "last_pickled": null,
 "max_active_runs": 16,
 "max_active_tasks": 16,
 "next_dagrun": "2022-06-18T00:00:00+00:00",
 "next_dagrun_create_after": "2022-06-18T00:00:00+00:00",
 "next_dagrun_data_interval_end": "2022-06-18T00:00:00",
 "next_dagrun_data_interval_start": "2022-06-18T00:00:00",
 "owners": [ "airflow" ],
 "pickle_id": null,
 "root_dag_id": null,
 "schedule_interval": {
 "__type": "CronExpression",
 "value": "@once"
 },
 "scheduler_lock": null,
 "tags": [ { "name": "example" }],
 "timetable_description": "Once, as soon as possible"
}
```

* ### List ALL variable
```SQL
curl -X GET --user "airflow:airflow" http://localhost:8080/api/v1/variables
```

* ## DAG Dependencies
* ### How to Execute DAG
* Periodic Execution: Specified with a schedule using 'Schedule'
* Triggered by another DAG
  * Explicit Trigger: DAG A explicitly triggers DAG B (TriggerDagRunOperator)
  * Reactive Trigger: DAG B waits for DAG A to finish (ExternalTaskSensor)

```Python
#Implementing DAG A's tasks using the TriggerDagRunOperator:
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

trigger_B = TriggerDagRunOperator(
  taskI_id = "trigger_B"
  trigger_dag_id = "DAG name to be triggered"
```

## Spark

* the next-generation big data technology following Hadoop.
* offers a wide range of features related to big data processing.
* Components of Spark 3.0
![spark](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/Spark.PNG)

* ## Spark vs MapReduce
1. Memory vs. Disk:
   - Spark is fundamentally memory-based for data processing. It can resort to disk usage when memory becomes scarce.
   - MapReduce primarily relies on disk-based processing.

2. Supported Environments:
   - MapReduce operates exclusively on top of Hadoop (YARN).
   - Spark not only supports Hadoop (YARN) but also other distributed computing environments such as Kubernetes (K8s) and Apache Mesos.

3. Data Structures:
   - MapReduce primarily supports key-value-based data structures.
   - Spark supports data structures that are conceptually similar to Pandas DataFrames and can handle various data formats.

4. Supported Computing Types:
   - Spark supports various computing types, including batch data processing, stream data processing, SQL, machine learning, and graph analysis.
  

Certainly, here's a summary of the information about Spark's programming APIs:

**Spark Programming APIs**

- **RDD (Resilient Distributed Dataset)**
  - A low-level programming API that allows for fine-grained control over data.
  - However, it can lead to increased coding complexity.

- **DataFrame & Dataset (Similar to Pandas DataFrames)**
  - High-level programming APIs that are becoming increasingly popular.
  - Typically used for structured data manipulation.
  - When are DataFrame/Dataset necessary?
    - When performing ML feature engineering or using Spark ML.
    - When tasks cannot be accomplished with SQL alone.

**Spark SQL**
- **Spark SQL** processes structured data using SQL.
- It allows processing DataFrames with SQL, treating them like tables.
- Similar functionality is available in Pandas.
- It offers performance up to 100 times faster than Hive queries.
- In reality, it's not entirely true. Hive has also evolved to use memory in processing.
  - Hive: Disk -> Memory
  - Spark: Memory -> Disk
  - Presto: Memory -> Disk
 
 
 ![spark](https://github.com/jongjunkim/Data-Engineering-Study/blob/main/img/spark-datalake.PNG)


* ## To enable data parallel processing, you need the following:

**Data Distribution:**
- Data must be distributed first.
- In Hadoop, the data processing unit is a data block on disk, typically 128MB in size, determined by the `dfs.block.size` property in the `hdfs-site.xml` configuration.
- In Spark, these data blocks are called "partitions," and the default partition size is also 128MB.
- The property `spark.sql.files.maxPartitionBytes` controls the partition size when reading files from HDFS or similar storage systems.

**Concurrent Processing:**
- Once the data is divided, each partition is processed concurrently.
- In MapReduce, when dealing with a file composed of N data blocks, N Map tasks are executed in parallel to process them.
- In Spark, data is loaded into memory in partition-sized chunks, and Executors are assigned to handle each partition.

Shuffling in data processing refers to the need to move data between partitions. Shuffling can occur in the following scenarios:

1. **Explicit Partitioning:** When you explicitly create new partitions, such as reducing the number of partitions.

2. **System-Driven Shuffling:** Shuffling can be triggered by system operations like grouping, aggregation, or sorting.
   - For example, during aggregation, data may need to be reshuffled to group by a specific key.

When shuffling occurs, data is moved over the network, which can impact performance. The number of partitions generated during shuffling can be determined by the `spark.sql.shuffle.partitions` configuration setting, which defaults to 200, representing the maximum number of partitions. However, the actual number of partitions can vary based on the operation being performed, such as random, hashing partitioning, or range partitioning. For example, sorting typically uses range partitioning.

Additionally, shuffling can lead to data skew, where some partitions have significantly more data than others, causing potential performance issues.
