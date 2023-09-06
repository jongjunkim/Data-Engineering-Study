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
