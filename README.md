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
zaruba please addData dataLabel='["0", "1"]'

# train, manually
zaruba please runMlopsModelTrainer

# run API
zaruba please runMlopsApi # run on new panel

# predict data with label 0, 1, and 2
zaruba please predictData predictionTest='0-1' # should be okay
zaruba please predictData predictionTest='0-9' # should be failed, since the model only knows '0' and '1'

# run Airflow
zaruba please runMlopsAirflow

# add data
zaruba please addData dataLabel='["2", "3"]'

# wait until minutes 0, 5, 10, 15, 25, 30 ... or 55

# predict again
zaruba please predictData predictionTest='0-1' # should be okay
zaruba please predictData predictionTest='0-9' # 2 and 3 should works (at least perform better)
```