# ML Ops Example

Simple ML Ops using Airflow and Scikit learn

> WIP, only for learning purpose. Don't use it on production.

# Components

* `mlopsDataGenerator`: Create data for training
* `mlopsModelTrainer`: Model trainer, creating ML model `pickle`. Should be executed by `mlopsAirflow`'s `Docker Operator`, but can also be triggered manually.
* `mlopsApi`: API to serve ML model.
* `mlopsAirflow`: Orchestrator

# Why ML Ops

Your data is evolving. Old data become obsolete, new data emerged.

Thus, your ML Model should evolve as well.