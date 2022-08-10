import os
import json
import pandas as pd
import psycopg2 as pg
from cryptography.fernet import Fernet
from flask import Flask, request, Response
from flask_restful import Api
from http import HTTPStatus

from models.sql_query import build_query


app = Flask(__name__)
api = Api(app)

class Error(Exception):
    pass

class UnauthorizedException(Error):
    pass

class ForbiddenException(Error):
    pass

def error_handler(message: str, status_code: int = HTTPStatus.BAD_REQUEST) -> dict:
    failure_dict = {
        "result": "failure",
        "reason": "",
    }
    failure_dict.update({"reason": message})
    return Response(json.dumps(failure_dict), status_code.value)


def authentication_layer():
    headers = request.headers
    token = headers.get("api_key")

    if not token:
        raise UnauthorizedException

    key = Fernet(str.encode(os.getenv("PRIV_KEY")))

    decrypted_user_key = (key.decrypt(str.encode(token))).decode()
    decrypted_api_key = key.decrypt(str.encode(os.getenv("API_KEY"))).decode()

    if decrypted_user_key == decrypted_api_key:
        return True
    raise ForbiddenException


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


@app.route("/dag_id", methods=["POST"])
def dag_id(dag_id=None):

    dag_id=request.form['dag_id']
    try:
        authentication_layer()
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="dag_id", object_name=dag_id
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df
    except UnauthorizedException:
        return error_handler(f"Missing API KEY.", HTTPStatus.UNAUTHORIZED)
    except ForbiddenException:
        return error_handler(f"Wrong API KEY.", HTTPStatus.FORBIDDEN)


@app.route("/task_id", methods=["POST"])
def task_id(task_id=None):

    task_id=request.form['task_id']
    try:
        authentication_layer()
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="task_id", object_name=task_id
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df
    except UnauthorizedException:
        return error_handler(f"Missing API KEY.", HTTPStatus.UNAUTHORIZED)
    except ForbiddenException:
        return error_handler(f"Wrong API KEY.", HTTPStatus.FORBIDDEN)

@app.errorhandler(404)
def page_not_found(e):
    return error_handler(f"Route not found.", HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
