import os
import logging
import pandas as pd
import psycopg2 as pg
from cryptography.fernet import Fernet
from flask import Flask, request
from flask_restful import Api
from psycopg2.extensions import AsIs


app = Flask(__name__)
api = Api(app)


def authentication_layer():
    headers = request.headers
    token = headers.get("api_key")

    key = Fernet(str.encode(os.getenv("PRIV_KEY")))

    decrypted_user_key = (key.decrypt(str.encode(token))).decode()
    decrypted_api_key = key.decrypt(str.encode(os.getenv("API_KEY"))).decode()

    if decrypted_user_key == decrypted_api_key:
        return True
    return False


def retrieve_data_from_scheduling(env, object_id, object_name):
    """Connect to Scheduling database, execute SQL query and retrieve desired data."""

    creds = {
        "env": {
            "stg": {
                "database": os.getenv("DATABASE_STG"),
                "user": os.getenv("USER_STG"),
                "password": os.getenv("PASS_STG"),
                "host": os.getenv("HOST_STG"),
                "port": os.getenv("PORT_STG"),
            },
            "red": {
                "database": os.getenv("DATABASE_RED"),
                "user": os.getenv("USER_RED"),
                "password": os.getenv("PASS_RED"),
                "host": os.getenv("HOST_RED"),
                "port": os.getenv("PORT_RED"),
            },
            "black": {
                "database": os.getenv("DATABASE_BLACK"),
                "user": os.getenv("USER_BLACK"),
                "password": os.getenv("PASS_BLACK"),
                "host": os.getenv("HOST_BLACK"),
                "port": os.getenv("PORT_BLACK"),
            },
        }
    }

    cred = creds["env"].get(env)

    query = """
        select
        %(object_id)s,
        max(runs) count_runs,
        ceiling(avg(total_time)) average,
        ceiling(percentile_cont(0.5) within group (order by (total_time))) median, 
        ceiling(max(total_time)) maximum,
        ceiling(min(total_time)) minimum,
        ceiling(cast(stddev(total_time) as integer)) standard_deviation,
        ceiling(cast(variance(total_time) as bigint)) variance_,
        ceiling(((ceiling(percentile_cont(0.5) within group (order by (total_time))) + ceiling(cast(stddev(total_time) as integer)))/ceiling(percentile_cont(0.5) within group (order by (total_time))))*ceiling(percentile_cont(0.5) within group (order by (total_time)))*1.2) score
        from (
            select *, 
            row_number() over (partition by task_id, dag_id order by dag_id) runs, 
            extract(epoch from (end_date - start_date))/60 total_time 
            from task_instance
            where
            %(object_id)s in (%(object_name)s)
            and task_id not in ('start', 'end', 'check_end', 'end_failure', 'end.end_failure', 'end_success', 'end.end_success')
            and state in ('success')
            and start_date is not null
            and try_number != 0) ti
        group by %(object_id)s
        order by %(object_id)s;
	"""

    try:
        conn = pg.connect(
            database=cred.get("database"),
            user=cred.get("user"),
            password=cred.get("password"),
            host=cred.get("host"),
            port=cred.get("port"),
        )
        airflow_df = pd.read_sql(
            query,
            conn,
            params={"object_id": AsIs(object_id), "object_name": object_name},
        )
    except Exception as err:
        print(err)
    finally:
        conn.close()

    return airflow_df


@app.route("/dag_id/<dag_id>", methods=["GET"])
def dag_id(dag_id=None):

    if not authentication_layer():
        raise Exception
    else:
        args = request.args
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="dag_id", object_name=dag_id, env=args.get("env")
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")

        return airflow_replica_df


@app.route("/task_id/<task_id>", methods=["GET"])
def task_id(task_id=None):

    if not authentication_layer():
        raise Exception
    else:
        args = request.args
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="task_id", object_name=task_id, env=args.get("env")
        )

        airflow_replica_df["task_id"] = (
            airflow_replica_df["task_id"].str.split(".").str.get(-1)
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
