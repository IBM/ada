from cryptography.fernet import Fernet, InvalidToken
import app as application
from app import UnauthorizedException, ForbiddenException
import pytest
from unittest import mock

client = application.app.test_client()


def test_authentication_layer_unauthorized():
    with pytest.raises(UnauthorizedException):
        with application.app.test_request_context():
            application.authentication_layer()


def test_authentication_layer_forbidden(mocker):
    mocker.patch.object(Fernet, "__init__", side_effect=ForbiddenException)
    with pytest.raises(ForbiddenException):
        with application.app.test_request_context():
            application.authentication_layer()


def test_invalid_token():
    with pytest.raises(InvalidToken):
        with application.app.test_request_context(headers={"api_key": "wrong_api_key"}):
            application.authentication_layer()
