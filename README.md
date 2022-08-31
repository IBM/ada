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

<h1>Contents</h1>

- [Features](#features)
- [Business context](#business-context)
- [Usage](#usage)
	- [Metrics](#metrics)
- [API](#api)
- [Deployment](#deployment)
	- [Code Engine](#code-engine)
- [Engine compatibility](#engine-compatibility)
- [License](#license)

<h1>Business context</h1>

The amount of stuck pods became an increasing pain for us: whenever they happened, they would demand support requests followed by analysis that often resulted in simple and manual actions. Based on that, there arose a need to automate this process, in other words, to make us able to identify a stuck pod and take the appropriate action in a fully automatic way, transparent for both developer and user.

Well, but what is the best way to identify a stuck pod? The answer is simple: based on historical data, we can tell if something is taking longer than it should to run. That’s when the perfect opportunity arose to implement, for the first time, a **Serverless computing module**.

<h1>Usage</h1>

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
| standard_deviation  | Is my runtime too far from the average? |
| variance  | How far is my runtime from the average? |

One of the most powerful metric ADA retrieves is the **score**. It's calculated by:

$$score = (\frac{ median + standard\;deviation}{median}) \times median \times 1.2$$

The factor 1.2 was arbitrarily chosen in order to round up the score, acting like a safety factor.

<h1>API</h1>

<h1>Deployment</h1>

<h3>Code Engine</h3>

For more information, access https://cloud.ibm.com/docs/codeengine.

<h1>Engine compatibility</h1>

<h1>License</h1>