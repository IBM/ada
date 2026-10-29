import jinja2.ext
import jinja2.utils
from markupsafe import Markup

# jinjasql (unmaintained, latest 0.1.8) relies on jinja2.utils.Markup and the
# jinja2.ext.autoescape extension, both removed in Jinja2 3.1 (autoescape is
# built in since 2.10). Restore them so we can run on patched Jinja2 versions.
if not hasattr(jinja2.utils, "Markup"):
    jinja2.utils.Markup = Markup

if not hasattr(jinja2.ext, "autoescape"):

    class _AutoEscapeExtension(jinja2.ext.Extension):
        pass

    jinja2.ext.autoescape = _AutoEscapeExtension

from jinjasql import JinjaSql  # noqa: E402
from models.templates.templates import queries  # noqa: E402

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
