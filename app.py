import os
import json
import pandas as pd
from pandas.core.frame import DataFrame
import psycopg2 as pg
from cryptography.fernet import Fernet, InvalidToken
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


def error_handler(
    message: str, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
) -> Response:
    failure_dict = {
        "Result": "Failure",
        "Reason": "",
    }
    failure_dict.update({"Reason": message})
    return Response(json.dumps(failure_dict), status_code.value)


def authentication_layer() -> bool:
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


def retrieve_data_from_scheduling(
    object_id=None, object_name=None, query_select="base_query"
) -> DataFrame:
    """Connect to Scheduling database, execute SQL query and retrieve desired data."""

    params = {
        "object_id": object_id,
        "object_name": object_name,
        "query_select": query_select,
    }

    query = build_query(**params)

    try:
        conn = pg.connect(
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASS"),
            host=os.getenv("HOST"),
            port=os.getenv("API_PORT"),
        )
        airflow_df = pd.read_sql(query, conn)
    except pg.DatabaseError:
        raise pg.DatabaseError
    finally:
        conn.close()

    return airflow_df


@app.route("/all", methods=["GET"])
def all():

    try:
        authentication_layer()
        airflow_replica_df = retrieve_data_from_scheduling(query_select="all_query")
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df
    except UnauthorizedException:
        return error_handler("Missing API KEY.", HTTPStatus.UNAUTHORIZED)
    except (ForbiddenException, InvalidToken):
        return error_handler("Wrong API KEY.", HTTPStatus.FORBIDDEN)


@app.route("/dag_id/<dag_id>", methods=["GET"])
def dag_id(dag_id=None):

    try:
        authentication_layer()
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="dag_id", object_name=dag_id
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df
    except UnauthorizedException:
        return error_handler("Missing API KEY.", HTTPStatus.UNAUTHORIZED)
    except (ForbiddenException, InvalidToken):
        return error_handler("Wrong API KEY.", HTTPStatus.FORBIDDEN)


@app.route("/task_id/<task_id>", methods=["GET"])
def task_id(task_id=None):

    try:
        authentication_layer()
        airflow_replica_df = retrieve_data_from_scheduling(
            object_id="task_id", object_name=task_id
        )
        airflow_replica_df = airflow_replica_df.to_json(orient="records")
        return airflow_replica_df
    except UnauthorizedException:
        return error_handler("Missing API KEY.", HTTPStatus.UNAUTHORIZED)
    except (ForbiddenException, InvalidToken):
        return error_handler("Wrong API KEY.", HTTPStatus.FORBIDDEN)


@app.errorhandler(404)
def page_not_found(e):
    return error_handler("Route not found.", HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
