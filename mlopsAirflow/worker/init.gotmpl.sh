echo "Init mlopsAirflow worker"

airflow variables set "modelTrainerDockerUrl" '{{ .GetConfig "modelTrainerDockerUrl" }}'
airflow variables set "modelTrainerImage" '{{ .GetConfig "modelTrainerImage" }}'
airflow variables set "modelTrainerEnv" '{"MLOPS_MODEL_TRAINER_STORAGE": "/storage"}'
airflow variables set "modelTrainerMinDate" '2021-09-09 09:09:09'
airflow variables set "modelTrainerHostStorage" '{{ .GetRelativePath "../../mlopsStorage" }}'