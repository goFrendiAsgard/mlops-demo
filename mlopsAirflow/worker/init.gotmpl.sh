echo "Init mlopsAirflow worker"

airflow variables set "modelTrainerDockerUrl" "{{ .GetConfig "modelTrainerDockerUrl" }}"
airflow variables set "modelTrainerImage" "{{ .GetConfig "modelTrainerImage" }}"
airflow variables set "modelTrainerEnv" '{"MLOPS_MODEL_TRAINER_STORAGE": "/storage"}'