import pytest
from jinjasql import JinjaSql
from models import sql_query
from models.templates.templates import queries


def test_build_query_success(mocker):
	params = {
        "object_id": "object_id",
        "object_name": "object_name",
        "query_select": "base_query"
    }
	query = {"base_query": "SELECT {{object_id}} FROM table WHERE {{object_id}} = {{object_name}}"}
	expected = "SELECT object_id FROM table WHERE object_id = object_name"
	j = JinjaSql(param_style="pyformat")
	query, bind_params = j.prepare_query(query, params)
	mocker.patch("models.templates.templates", return_value=query)
	#mocker.patch.object(JinjaSql, "prepare_query", return_value=query)
	assert sql_query.build_query(**params) == query % bind_params
