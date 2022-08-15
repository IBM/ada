import app
from app import UnauthorizedException, ForbiddenException
import pytest
from unittest import mock

client = app.app.test_client()

# def test_success():
#     app.authentication_layer = mock.MagicMock(return_value=True)
#     #app.airflow_replica_df = mock.MagicMock(return_value=True)
#     response = client.get('/task_id/task_id')
#     assert response.status_code == 200

def test_authentication_layer():
    token = None
    with pytest.raises(UnauthorizedException):
        app.authentication_layer()
    assert token == None
