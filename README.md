# ML Ops Example

Simple ML Ops using Airflow and Scikit learn

> WIP, only for learning purpose. Don't use it on production.

# Components

* `mlopsDataGenerator`: Create data for training
    - Ports: 
        - http: `3000`
    - Mount volume: -
* `mlopsModelTrainer`: Model trainer, creating ML model `pickle`. Should be executed by `mlopsAirflow`'s `Docker Operator`, but can also be triggered manually.
    - Ports: -
    - Mount volumes: 
        - /storage: `mlopsStorage`
* `mlopsApi`: API to serve ML model.
    - Ports:
        - http: `8000`
    - Mount volumes: 
        - /storage: `mlopsStorage`
* `mlopsAirflow`: Orchestrator
    - Ports:
        - http (web UI): `8080`
        - http (flower): `5555`
    - Mount volumes:
        - /opt/airflow/dags: `mlopsAirflow/dags`
        - /storage: `mlopsStorage`
# Why ML Ops

Your data is evolving. Old data become obsolete, new data emerged.

Thus, your ML Model should evolve as well.