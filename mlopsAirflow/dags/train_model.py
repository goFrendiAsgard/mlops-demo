from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from modelTrainer.main import train
from airflow.models import Variable

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'modelTrainer',
    'depend_on_past'        : False,
    'start_date'            : datetime(2018, 1, 3),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

storage_path = Variable.get(key='modelTrainerStoragePath')
min_date_time = Variable.get(key='modelTrainerMinDateTime')

with DAG('modelTrainer_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:

    t1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Hello"'
    )

    def train_task(ds, **kwargs):
        train(storage_path, min_date_time, '{{ execution_date.to_datetime_string() }}')

    t2 = PythonOperator(
        task_id='modelTrainer_docker_command',
        python_callable=train_task
    )

    t3 = BashOperator(
        task_id="change_permission",
        bash_command=f"chmod 777 {storage_path}/*.*"
    )

    t1 >> t2 >> t3