# ML Ops Example

Simple ML Ops using Airflow and Scikit learn

> WIP, only for learning purpose. Don't use it on production.

# Components

* `mlopsDataGenerator`: Create data for training
    - Ports: 
        - http: `3000`
    - Mount volume: -
* `mlopsModelTrainer`: Model trainer, creating ML model `pickle`. Should be executed by `mlopsAirflow`'s `DAG`, but can also be triggered manually.
    - Ports: -
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
        - /opt/airflow/storage: `mlopsStorage`
# Why ML Ops

Your data is evolving. Old data become obsolete, new data emerged.

Thus, your ML Model should evolve as well.

# Demo

```sh
# generate data with labels 0 and 1
zaruba please runMlopsDataGenerator # run on new panel
zaruba please addData1.sh # new panel

# train, manually
zaruba please runMlopsModelTrainer

# run API
zaruba please runMlopsApi # run on new panel

# predict data with label 0, 1, and 2
zaruba please predict0
zaruba please predict1
zaruba please predict2 # this one should fail because we don't have the data yet

# run Airflow
zaruba please runMlopsAirflow

# add data
zaruba please addData2.sh

# wait until minutes 0, 5, 10, 15, 25, 30 ... or 55

# predict again
zaruba please predict0
zaruba please predict1
zaruba please predict2 # now it should works
```