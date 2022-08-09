import os
import pandas as pd
import psycopg2 as pg
from cryptography.fernet import Fernet
from flask import Flask, request
from flask_restful import Api

from models.sql_query import build_query


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


def retrieve_data_from_scheduling(object_id, object_name):
    """Connect to Scheduling database, execute SQL query and retrieve desired data."""

    params = {
        "object_id": object_id,
        "object_name": object_name,
    }

    query = build_query(**params)

    try:
        conn = pg.connect(
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASS"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
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
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="dag_id", object_name=dag_id
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")

        return airflow_replica_df


@app.route("/task_id/<task_id>", methods=["GET"])
def task_id(task_id=None):

    if not authentication_layer():
        raise Exception
    else:
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="task_id", object_name=task_id
        )

        airflow_replica_df["task_id"] = (
            airflow_replica_df["task_id"].str.split(".").str.get(-1)
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
