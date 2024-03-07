DAG_QUERY = """
		select
		{{object_id}},
		count(dag_id) count_runs,
		ceiling(avg(total_time)) average,
		ceiling(percentile_cont(0.5) within group (order by (total_time))) median, 
		ceiling(max(total_time)) maximum,
		ceiling(min(total_time)) minimum,
		ceiling(stddev(total_time)) standard_deviation,
		ceiling(variance(total_time)) variance_,
		ceiling((avg(total_time) + {{stddev_multiplier}}*ceiling(stddev(total_time)))*{{score_threshold}}) score
		from (select dag_id,
			count(*) over (partition by dag_id) as _count_rows,
			row_number() over (partition by dag_id order by end_date desc) as _row_number,
			extract(epoch from (end_date - start_date))/60 total_time 
			from dag_run
			where
			{{object_id}} in ('{{object_name}}')
			and state in ('success')
			and start_date is not null) dr
		where total_time > {{outlier_min}}
		and total_time < {{outlier_max}}
        and _row_number <= {{limit}}
		group by {{object_id}}
		order by {{object_id}};
	"""

TASK_QUERY = """
		select
		{{object_id}},
        dag_id,
		count(task_id) count_runs,
		ceiling(avg(total_time)) average,
		ceiling(percentile_cont(0.5) within group (order by (total_time))) median, 
		ceiling(max(total_time)) maximum,
		ceiling(min(total_time)) minimum,
		ceiling(stddev(total_time)) standard_deviation,
		ceiling(variance(total_time)) variance_,
		ceiling((avg(total_time) + {{stddev_multiplier}}*ceiling(stddev(total_time)))*{{score_threshold}}) score
		from (select task_id, dag_id,
			count(*) over (partition by task_id) as _count_rows,
			row_number() over (partition by task_id order by end_date desc) as _row_number,
			extract(epoch from (end_date - start_date))/60 total_time 
			from task_instance
			where
			{{object_id}} in ('{{object_name}}')
            and dag_id in ('{{dag_id}}')
			and operator = 'CrdTriggerOperator'
			and state in ('success')
			and start_date is not null
			and try_number != 0) ti
		where total_time > {{outlier_min}}
		and total_time < {{outlier_max}}
		and _row_number <= {{limit}}
		group by {{object_id}}, dag_id
		order by {{object_id}};
	"""


ALL_QUERY = """
		select
		task_id,
        dag_id,
		max(runs) count_runs,
		ceiling(avg(total_time)) average,
		ceiling(percentile_cont(0.5) within group (order by (total_time))) median, 
		ceiling(max(total_time)) maximum,
		ceiling(min(total_time)) minimum,
		ceiling(stddev(total_time)) standard_deviation,
		ceiling(variance(total_time)) variance_,
		ceiling((avg(total_time) + {{stddev_multiplier}}*ceiling(stddev(total_time)))*{{score_threshold}}) score
		from (
			select *, 
			row_number() over (partition by task_id, dag_id order by dag_id) runs, 
			extract(epoch from (end_date - start_date))/60 total_time 
			from task_instance
			where
			task_id not in ('start', 'end', 'check_end', 'end_failure', 'end.end_failure', 'end_success', 'end.end_success')
			and state in ('success')
			and start_date is not null
			and try_number != 0) ti
		group by task_id, dag_id
		order by task_id;
	"""

queries = {
    "dag_query": DAG_QUERY,
    "task_query": TASK_QUERY,
    "all_query": ALL_QUERY,
}
