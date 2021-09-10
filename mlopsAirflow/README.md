# Airflow Artefact

Airflow is a platform created by the community to programmatically author, schedule and monitor workflows.

With Zaruba you can manage your airflow DAG and run it in your local computer seemlessly.

## Run airflow

To run Airflow in your local computer you can invoke:

```sh
zaruba please runMlopsAirflow
```

By invoking the command, you will also run several containers:

* `mlopsRedis`: Redis, for caching and stuffs
* `mlopsPostgre`: Posgre, for airflow persistance storage
* `mlopsAirflowConfigurator`: A container that run before any other airflow containers. Through this container, Zaruba should set up the database and anything else. It will also run your custom script (see: `configurator/init.gotmpl.sh`).
* `mlopsAirflowWebServer`: The web server, by default run on port `8080`. To change this, you should edit `mlopsAirflowWebServer`'s `port` value at `../zaruba-tasks/mlopsAirflow/config.zaruba.yaml`.
* `mlopsAirflowScheduler`: The scheduler.
* `mlopsAirflowWorker`: The one that really run the task.
* `mlopsAirflowFlower`: The one that monitor `celery` messaging. By default run on port `5555`. To change this, you should edit `mlopsAirflowFlower`'s `port` value at `../zaruba-tasks/mlopsAirflow/config.zaruba.yaml`.

> 💡 To see how airflow really works, please visit [this article](https://airflow-tutorial.readthedocs.io/en/latest/airflow-intro.html)

## Add your DAG

You can simply put your DAG on `dags` directory.

## Setup Airflow

To setup custom configuration in your airflow instance, you will need to modify:

* `mlopsAirflow/configurator/init.gotmpl.sh`
* `mlopsAirflow/worker/init.gotmpl.sh`
