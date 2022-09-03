<p align="center">
    <img src="https://media.github.ibm.com/user/376942/files/7bb5fe80-231a-11ed-8440-8c14e1e3c289" height="160">
    <h1 align="center">Airflow DAG Analytics</h1>
</p>

<p align="center">
  <a href="https://airflow.apache.org/">
    <img alt="Airflow" src="https://img.shields.io/static/v1?label=MADE+FOR&message=AIRFLOW&color=017CEE&logo=Apache+Airflow" />
  </a>
</p>

<!-- <h1><img height="20" src="https://media.github.ibm.com/user/376942/files/ebc48480-231a-11ed-8b70-30e2b8893504">&nbsp;&nbsp;What is ADA?</h1> -->

ADA is a microservice created to retrieve key analytics metrics for task and DAG level from your Airflow database instance.

<h1>Features</h1>

Highly integrated with Airflow, ADA makes you able to retrieve data from your database and get analytical insights from it. By plugging ADA in your instance, you will get metrics that can help you to make decisions based on your DAGs historical behavior. 

With ADA, you will be able to:

1. Identify stuck pods
2. Monitor DAGs and tasks performance
3. Analyze outliers

# Contents

- [Features](#features)
- [Business context](#business-context)
- [Usage](#usage)
	- [Metrics](#metrics)
  - [Deployment](#deployment)
- [API reference](#api-reference)
- [Engine compatibility](#engine-compatibility)
- [Contributing](#contributing)
- [License](#license)

# Business context

Stuck pods may become a huge pain for developers: whenever they happen, they always demand attention. Based on that, ADA was born to provide a solution for those who want historical data about their DAGs. It means ADA enables you to identify if a pod is taking longer than it should, and then make quick decisions.

ADA can be fully decoupled from your code, which is great when you use an autoscaling tool to host it. 

# Usage

By deploying ADA, it becomes accessible to any other component you may want to communicate with.

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
    <img src="https://latex.codecogs.com/svg.image?score%20=%20(%5Cfrac%7B%20median%20&plus;%20standard%5C;deviation%7D%7Bmedian%7D)%20%5Ctimes%20median%20%5Ctimes%201.2" height="45">
</p>

&nbsp;

The score is the main metric you must analyze and rely on when identifying a stuck pod. You can use it as your threshold to decide to take - or not - an action about that run. The factor **1.2** was arbitrarily chosen in order to round up the score, acting like a <ins>safety factor</ins>. It makes the metric more trustable and robust, since it's less susceptible to outliers.

## Deployment

When deploying ADA, make sure you have set all required environment variables. You will need two different types of them:

1. **Authorization**
    
    In order to encrypt/decrypt your keys, you need to set your `PRIV_KEY` and `API_KEY`. It's important to mention that ADA follows the [Fernet implementation](https://cryptography.io/en/latest/fernet/) style. 

2. **Airflow database (Postgres)**

    In order to access your Airflow database (Postgres supported), you need to add all of your connection settings. It includes: database, host, username, password and port. Check [psycopg](https://www.psycopg.org/docs/) documentation for more details.

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

- Successfully deployed in [IBM Code Engine](https://cloud.ibm.com/docs/codeengine), [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) and [Microsoft Azure Functions](https://azure.microsoft.com/pt-br/services/functions/#overview).

# Contributing

Contributions are always welcome!

See `docs/contributing.md` for ways to get started.

# License