from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from docker.types import Mount

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'modelTrainer DockerOperator',
    'depend_on_past'        : False,
    'start_date'            : datetime(2018, 1, 3),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

docker_url = Variable.get(key='modelTrainerDockerUrl')
docker_operator_image = Variable.get(key='modelTrainerImage')
docker_operator_environment = Variable.get(key='modelTrainerEnv', deserialize_json=True)

with DAG('modelTrainer_docker_dag', default_args=default_args, schedule_interval='5 * * * *', catchup=False) as dag:

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
    )

    # see: https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/_api/airflow/providers/docker/operators/docker/index.html#module-airflow.providers.docker.operators.docker
    t2 = DockerOperator(
        task_id='modelTrainer_docker_command',
        image=docker_operator_image,
        api_version='auto',
        auto_remove=True,
        environment={ 
            "MLOPS_MODEL_TRAINER_MIN_DATE": "2021-09-09 09:09:09",
            "MLOPS_MODEL_TRAINER_MAX_DATE": "{{ execution_date..to_datetime_string() }}",
            **docker_operator_environment,
        },
        docker_url=docker_url,
        mounts=Mount(
            target="/storage",
            source="/storage",
        )
    )

    t3 = BashOperator(
        task_id='print_done',
        bash_command='echo "Done"'
    )

    t1 >> t2 >> t3