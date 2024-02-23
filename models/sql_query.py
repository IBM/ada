from jinjasql import JinjaSql
from models.templates.templates import queries


def build_query(**params):

    params = {
        "object_id": params.get("object_id"),
        "object_name": params.get("object_name"),
        "query_select": params.get("query_select"),
        "outlier_min": params.get("outlier_min"),
        "outlier_max": params.get("outlier_max"),
        "limit": params.get("limit"),
        "stddev_multiplier": params.get("stddev_multiplier"),
        "score_threshold": params.get("score_threshold"),
        "dag_id": params.get("dag_id"),
    }

    query_template = queries.get(params.get("query_select"))

    j = JinjaSql(param_style="pyformat")
    query, bind_params = j.prepare_query(query_template, params)

    return query % bind_params
