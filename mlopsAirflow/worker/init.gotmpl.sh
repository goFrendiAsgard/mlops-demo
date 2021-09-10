echo "Init mlopsAirflow worker"

airflow variables set "modelTrainerMinDateTime" '2021-09-09 09:09:09'
airflow variables set "modelTrainerStoragePath" '/opt/airflow/storage'