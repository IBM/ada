<p align="center">
    <img src="https://user-images.githubusercontent.com/79098111/190011612-201a77aa-1111-45fe-937c-e994d3fdafa8.png" height="160">
    <h1 align="center">Airflow DAG Analytics</h1>
</p>

<p align="center">
  <a href="https://airflow.apache.org/">
    <img alt="Airflow" src="https://img.shields.io/static/v1?label=MADE+FOR&message=AIRFLOW&color=017CEE&logo=Apache+Airflow" />
  </a>
</p>

ADA is a microservice created to retrieve key analytics metrics for task and DAG level from your Airflow database instance.

Highly integrated with Airflow, ADA makes you able to retrieve data from your database and get analytical insights from it. By plugging ADA in your instance, you will get metrics that can help you to make decisions based on your DAGs historical behavior. 

ADA was born to provide a solution for those who want historical data about their DAGs. It can be fully decoupled from your code, which is great when you use an autoscaling tool to host it. 

# Contents

- [Usage](#usage)
	- [Metrics](#metrics)
  - [Deployment](#deployment)
  - [Use cases](#use-cases)
    - [Stuck pods](#stuck-pods)
    - [DAG Predict](#dag-predict)
- [API reference](#api-reference)
- [Engine compatibility](#engine-compatibility)
- [Contributing](#contributing)
- [License](#license)

# Usage
## Metrics

Using current ADA's SQL queries you can get the following information:

| Metric  | Insight  |
| ------------ | ------------ |
| score  | Is it taking longer than expected?  |
| average  | What is its average duration?  |
| count_runs  | How many times did it run?  |
| maximum  | What is its longest duration?  |
| minimum  | What is its shortest duration?  |
| median | What is the median duration?  |
| standard_deviation  | How often is my duration far from the average? |
| variance  | How far is my duration from the average? |

One of the most powerful metric ADA retrieves is the **score**. It's calculated by:

&nbsp;

<p align="center">
    <img src="https://media.github.ibm.com/user/376942/files/e7bcdd00-3383-11ed-8d3d-7f5772c73e72" height="45">
</p>

&nbsp;

The score is the main metric you must analyze and rely on when identifying a stuck pod. You can use it as your threshold to decide to take - or not - an action about that run. The factor **1.2** was arbitrarily chosen in order to round up the score, acting like a <ins>safety factor</ins>. It makes the metric more trustable and robust, since it's less susceptible to outliers.

## Deployment

When deploying ADA, make sure you have set all required environment variables. You will need two different types of them:

1. **Authorization**
    
    In order to encrypt/decrypt your keys, you need to set your `PRIV_KEY` and `API_KEY`. It's important to mention that ADA follows the [Fernet implementation](https://cryptography.io/en/latest/fernet/) style. 

2. **Airflow database (Postgres)**

    In order to access your Airflow database (Postgres supported), you need to add all of your connection settings. It includes: database, host, username, password and port. Check [psycopg](https://www.psycopg.org/docs/) and [IBM Cloud Databases for PostgreSQL](https://www.ibm.com/cloud/databases-for-postgresql) for more details.

If nothing is missing, your docker run command when testing locally should look like this:

 ```docker
  docker run --name ada -p 7000:7000 --rm \
    -e DATABASE=$DATABASE \
    -e USER=$USER \
    -e PASS=$PASS \
    -e HOST=$HOST \
    -e PORT=$PORT \
    -e PRIV_KEY=$PRIV_KEY \
    -e API_KEY=$API_KEY \
    -i -t ada bash
  ```

## Use cases

Here are some great examples on how ADA can make you life a lot easier :)

### Stuck pods

If you're working integrated with [Apache Spark](https://spark.apache.org/), there's a chance **stuck pods** are a big pain for you. Whenever they happen, they always require attention and quick actions. With ADA, you'll have the metrics at hand! It means you can use the **score** to tell if it's taking longer - or not - than it should to run. Your workflow could look like this:

<p align="center">
    <img src="https://media.github.ibm.com/user/376942/files/e034c580-305d-11ed-974e-45eace3cf971">
</p>

### DAG Predict

If you wish to predict you DAGs duration, ADA can help you with that as well! By using the metrics ADA provide, you will be able to tell what is the average runtime of a specific DAG. It means your process can be more transparent and reliable.

If you still want to go further, ADA can provide the numbers to your machine learning model, such as an echo state network, or a math approach you design on your own!

<p align="center">
    <img src="https://media.github.ibm.com/user/376942/files/e891fe00-3067-11ed-8232-64693b505e71">
</p>

# API reference

### /all

Return all combinations of `task_id` and `dag_id` in your database instance.

#### Request
```http
  GET /all
```

#### Response
 ```json
 [
    {
        "task_id": "task_id_α",
        "dag_id": "dag_id_α",
        "count_runs": 1,
        "average": 1,
        "median": 1,
        "maximum": 1,
        "minimum": 1,
        "standard_deviation": 1,
        "variance_": 1,
        "score": 1
    },
    ...,
    {
        "task_id": "task_id_β",
        "dag_id": "dag_id_β",
        "count_runs": 2,
        "average": 2,
        "median": 2,
        "maximum": 2,
        "minimum": 2,
        "standard_deviation": 2,
        "variance_": 2,
        "score": 2
    }
]
 ```

* * *

### /dag_id

Return metrics in a **DAG** level.

#### Request
```http
  GET /dag_id/<your_dag_id>
```

#### Response
 ```json
 [
    {
        "dag_id": "dag_id_α",
        "count_runs": 1,
        "average": 1,
        "median": 1,
        "maximum": 1,
        "minimum": 1,
        "standard_deviation": 1,
        "variance_": 1,
        "score": 1
    }
]
 ```

* * *

### /task_id

Return metrics in a **task** level.

#### Request
```http
  GET /task_id/<your_task_id>
```

#### Response
 ```json
 [
    {
        "task_id": "task_id_α",
        "count_runs": 1,
        "average": 1,
        "median": 1,
        "maximum": 1,
        "minimum": 1,
        "standard_deviation": 1,
        "variance_": 1,
        "score": 1
    }
]
 ```

# Engine compatibility

- Ready to be a **Serverless API**! 
- Successfully deployed in [IBM Code Engine](https://cloud.ibm.com/docs/codeengine).

# Contributing

Contributions are always welcome!

See [contributing.md](https://github.com/IBM/ada/blob/master/docs/contributing.md) for ways to get started.

# License

 ```
Copyright 2022 - IBM Inc. All rights reserved
SPDX-License-Identifier: Apache 2.0
 ```

See [LICENSE](https://github.com/IBM/ada/blob/master/LICENSE) for the full license text.