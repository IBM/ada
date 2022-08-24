import pytest
from models import sql_query
from models.templates.templates import queries

#print("---->", globals())

def test_build_query_success(mocker):
	jinja_mock = mocker.patch("models.sql_query.JinjaSql", autospec=True)
	j = jinja_mock.return_value
	params = {
        "object_id": "object_id",
        "object_name": "object_name",
        "query_select": "base_query"
    }
	query = "SELECT {{object_id}} FROM table WHERE {{object_id}} = {{object_name}}"
	mocker.patch("models.templates.templates", return_value=query)
	j.prepare_query.return_value = (query, params)
	assert sql_query.build_query(**params) == j.prepare_query.return_value
