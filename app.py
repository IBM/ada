import os
import logging
import pandas as pd
import psycopg2 as pg
from cryptography.fernet import Fernet
from flask import Flask, request
from flask_restful import Api
from psycopg2.extensions import AsIs

from sql_query import build_query


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

    params = {
        "object_id": object_id,
        "object_name": object_name,
    }

    query = build_query(**params)

    try:
        conn = pg.connect(
            database=cred.get("database"),
            user=cred.get("user"),
            password=cred.get("password"),
            host=cred.get("host"),
            port=cred.get("port"),
        )
        airflow_df = pd.read_sql(query, conn)
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
