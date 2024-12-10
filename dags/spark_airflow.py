import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

dag = DAG(
    dag_id="sparkingflow",
    default_args={
        "owner": "Or Hasson",
        "start_date": airflow.utils.dates.days_ago(1),
    },
    schedule_interval="@daily",
)

start = PythonOperator(
    task_id="start",
    python_callable=lambda: print("Jobs started"),
    dag=dag
)

python_job = SparkSubmitOperator(
    task_id="python_job",
    conn_id="spark-conn",
    application="jobs/python/wordcountjob.py",
    dag=dag
)

scala_job = SparkSubmitOperator(
    task_id="scala_job",
    conn_id="spark-conn",
    application="jobs/scala/target/scala-2.12/word-count_2.12-0.1.jar",
    java_class="WordCount",
    name="scala-word-count",
    dag=dag
)

java_job = SparkSubmitOperator(
    task_id="java_job",
    conn_id="spark-conn",
    application="jobs/java/java-spark/target/spark-job-1.0-SNAPSHOT.jar",
    java_class="com.airscholar.spark.WordCount",
    name="java-word-count",
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable=lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> [python_job, scala_job] >> end
