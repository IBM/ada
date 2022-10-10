import pytest
from models import sql_query


def test_build_query_success(mocker):
	params = {
        "object_id": "object_id",
        "object_name": "object_name",
        "query_select": "base_query"
    }
	query = {"base_query": "SELECT {{object_id}} FROM table WHERE {{object_id}} = {{object_name}}"}
	mocker.patch.dict("models.templates.templates.queries", query)
	assert sql_query.build_query(**params) == "SELECT object_id FROM table WHERE object_id = object_name"