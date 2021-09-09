if [ -z "${MLOPS_DATA_GENERATOR_HTTP_PORT}" ]
then
    MLOPS_DATA_GENERATOR_HTTP_PORT=3000
fi

if [ -n "${MLOPS_DATA_GENERATOR_SSL_CERT_FILE}" ] && [ -n "$MLOPS_DATA_GENERATOR_SSL_KEY_FILE" ]
then
    pipenv run uvicorn main:app --host=0.0.0.0 --ssl-keyfile "${MLOPS_DATA_GENERATOR_SSL_KEY_FILE}" --ssl-certfile "${MLOPS_DATA_GENERATOR_SSL_CERT_FILE}" --port=${MLOPS_DATA_GENERATOR_HTTP_PORT}
else
    pipenv run uvicorn main:app --host=0.0.0.0 --port=${MLOPS_DATA_GENERATOR_HTTP_PORT}
fi