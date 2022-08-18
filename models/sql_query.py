from jinjasql import JinjaSql
from models.templates.templates import queries

def build_query(**params):

    params = {
        "object_id": params.get("object_id"),
        "object_name": params.get("object_name"),
        "query_select": params.get("query_select")
    }

    query_template = queries.get(params.get("query_select"))

    
    j = JinjaSql(param_style="pyformat")
    query, bind_params = j.prepare_query(query_template, params)

    return query % bind_params
