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

ADA is a microservice created to retrieve key analytics metrics for task and dag level from your Airflow database instance.

<h1>Features</h1>

Highly integrated with Airflow, ADA makes you able to retrieve data from your database and get analytical insights from it. By plugging ADA in your instance, you will get metrics that can help you to make decisions based on your DAGs historical behavior. 

With ADA, you will be able to:

1. Identify stuck pods
2. Monitor DAGs and tasks performance
3. Analyze outliers

<h1>Contents</h1>

- [Features](#features)
- [Business context](#business-context)
- [Usage](#usage)
	- [Metrics](#metrics)
- [API reference](#api-reference)
- [Deployment](#deployment)
	- [Code Engine](#code-engine)
- [Engine compatibility](#engine-compatibility)
- [License](#license)

<h1>Business context</h1>

Stuck pods may become a huge pain for developers: whenever they happen, they always demand attention. Based on that, ADA was born to provide historical data about runtime. It means ADA enables you to identify if a pod is taking longer than it should, and then make quick decisions.

ADA can be fully decoupled from your code, which is great when you use an autoscaling tool to host it. 

<h1>Usage</h1>

By deploying ADA, it becomes accessible to any other component you may wat to communicate with.

<h2>Metrics</h2>

Using ADA's SQL query you can get the following information:

| Metric  | Insight  |
| ------------ | ------------ |
| score  | Is it taking longer than expected?  |
| average  | What is its average runtime?  |
| count_runs  | How many times did it run?  |
| maximum  | What is its longest runtime?  |
| minimum  | What is its shortest runtime?  |
| median | What is the median runtime?  |
| standard_deviation  | How often is my runtime far from the average? |
| variance  | How far is my runtime from the average? |

One of the most powerful metric ADA retrieves is the **score**. It's calculated by:

&nbsp;

<p align="center">
    <img src="https://latex.codecogs.com/svg.image?score%20=%20(%5Cfrac%7B%20median%20&plus;%20standard%5C;deviation%7D%7Bmedian%7D)%20%5Ctimes%20median%20%5Ctimes%201.2" height="45">
</p>

&nbsp;

The factor **1.2** was arbitrarily chosen in order to round up the score, acting like a <ins>safety factor</ins>. It gives the metric more trustable and robust, since it's less susceptible to outliers.

<h1>API reference</h1>

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

<h1>Deployment</h1>

<h3>Code Engine</h3>

For more information, access https://cloud.ibm.com/docs/codeengine.

<h1>Engine compatibility</h1>

<h1>License</h1>