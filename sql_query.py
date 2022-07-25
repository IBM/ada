from jinjasql import JinjaSql


def build_query(object_id, object_name):

    params = {
        "object_id": object_id,
        "object_name": object_name,
    }

    query_template = """
		select
		{{object_id}},
		max(runs) count_runs,
		ceiling(avg(total_time)) average,
		ceiling(percentile_cont(0.5) within group (order by (total_time))) median, 
		ceiling(max(total_time)) maximum,
		ceiling(min(total_time)) minimum,
		ceiling(cast(stddev(total_time) as integer)) standard_deviation,
		ceiling(cast(variance(total_time) as bigint)) variance_,
		ceiling(((ceiling(percentile_cont(0.5) within group (order by (total_time))) + ceiling(cast(stddev(total_time) as integer)))/ceiling(percentile_cont(0.5) within group (order by (total_time))))*ceiling(percentile_cont(0.5) within group (order by (total_time)))*1.2) score
		from (
			select *, 
			row_number() over (partition by task_id, dag_id order by dag_id) runs, 
			extract(epoch from (end_date - start_date))/60 total_time 
			from task_instance
			where
			{{ object_id }} in ('{{ object_name }}')
			and task_id not in ('start', 'end', 'check_end', 'end_failure', 'end.end_failure', 'end_success', 'end.end_success')
			and state in ('success')
			and start_date is not null
			and try_number != 0) ti
		group by {{ object_id }}
		order by {{ object_id }};
	"""

    j = JinjaSql(param_style="pyformat")
    query, bind_params = j.prepare_query(query_template, params)

    print(query)
    print(bind_params)
    print(query % bind_params)

    return query % bind_params
