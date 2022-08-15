import app
from app import UnauthorizedException, ForbiddenException
import unittest
import pytest
from unittest.mock import MagicMock

client = app.app.test_client()

# def test_success():
#     app.authentication_layer = mock.MagicMock(return_value=True)
#     #app.airflow_replica_df = mock.MagicMock(return_value=True)
#     response = client.get('/task_id/task_id')
#     assert response.status_code == 200

# def test_authentication_layer(mocker):
#     mocker.patch.object(requests, "request", return_value=None)
#     with pytest.raises(UnauthorizedException):
#         app.authentication_layer()

def test_retrieve_data_from_scheduling_error():
	with pytest.raises(Exception) as excinfo:
		app.retrieve_data_from_scheduling('anything', 'anything')
	assert str(excinfo.value) == 'some info'
