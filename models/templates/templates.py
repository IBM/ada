
BASE_QUERY = """
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
			{{object_id}} in ('{{object_name}}')
			and task_id not in ('start', 'end', 'check_end', 'end_failure', 'end.end_failure', 'end_success', 'end.end_success')
			and state in ('success')
			and start_date is not null
			and try_number != 0) ti
		group by {{object_id}}
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
		ceiling(cast(stddev(total_time) as integer)) standard_deviation,
		ceiling(cast(variance(total_time) as bigint)) variance_,
		ceiling(((ceiling(percentile_cont(0.5) within group (order by (total_time))) + ceiling(cast(stddev(total_time) as integer)))/ceiling(percentile_cont(0.5) within group (order by (total_time))))*ceiling(percentile_cont(0.5) within group (order by (total_time)))*1.2) score
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
    "base_query": BASE_QUERY,
    "all_query" : ALL_QUERY,     
}