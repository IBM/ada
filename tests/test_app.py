from cryptography.fernet import Fernet, InvalidToken
import app as application
from app import UnauthorizedException, ForbiddenException
import json
import pytest
import psycopg2 as pg
import pandas as pd
from unittest import mock
from http import HTTPStatus

client = application.app.test_client()


class PostgreMock:
    def close(self):
        return True


def test_error_handler(mocker):
    expected_dict = {
        "Result": "Failure",
        "Reason": "Invalid request.",
    }
    with application.app.test_request_context():
        res = application.error_handler(message="Invalid request.", status_code=HTTPStatus.BAD_REQUEST)
        assert json.loads(res.response[0]) == expected_dict
        assert res.status_code == 400


def test_authentication_layer_success(mocker):
    mocker.patch.object(Fernet, "__init__", return_value=None)
    mocker.patch.object(Fernet, "decrypt", return_value="valid_api_key".encode())
    with application.app.test_request_context(headers={"api_key": "valid_api_key"}):
        application.authentication_layer()


def test_authentication_layer_unauthorized():
    with pytest.raises(UnauthorizedException):
        with application.app.test_request_context():
            application.authentication_layer()


def test_authentication_layer_forbidden(mocker):
    mocker.patch.object(Fernet, "__init__", side_effect=ForbiddenException)
    with pytest.raises(ForbiddenException):
        with application.app.test_request_context(headers={"api_key": "wrong_api_key"}):
            application.authentication_layer()


def test_authentication_layer_invalid_token():
    with pytest.raises(InvalidToken):
        with application.app.test_request_context(headers={"api_key": "wrong_api_key"}):
            application.authentication_layer()


def test_retrieve_data_from_scheduling_success(mocker):
    data = [1, 2, 3]
    df = pd.DataFrame(data, columns=["Numbers"])
    mocker.patch.object(pg, "connect", return_value=PostgreMock())
    mocker.patch.object(pd, "read_sql", return_value=df)
    with application.app.test_request_context():
        df = application.retrieve_data_from_scheduling(
            object_id="object_id", object_name="object_name"
        )


def test_retrieve_data_from_scheduling_database_error(mocker):
    mocker.patch.object(pg, "connect", return_value=PostgreMock())
    mocker.patch.object(pd, "read_sql", side_effect=pg.DatabaseError)
    with pytest.raises(pg.DatabaseError):
        with application.app.test_request_context():
            application.retrieve_data_from_scheduling(
                object_id="object_id", object_name="object_name"
            )
