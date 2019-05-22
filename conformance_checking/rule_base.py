from typing import List, Any


def get_percentage(total: int, observations: int) -> float:
	return (100/total) * observations


def check_cardinality(log, activity: str, upper: int, lower: int) -> dict:
	"""

	:param: process log
	:param activity: name of the activity
	:param upper: max. number of occurrence in one trace, -1 if infinite
	:param lower: min. number of occurrence in one trace
	:return: 
	"""

	violation_upper = 0
	violation_lower = 0

	for trace in log:

		events = trace['events']
		counter = events.count(activity)

		if counter < lower:
			violation_lower += 1
		elif counter > upper != -1:
			violation_upper += 1

	return {'activity': activity,
			'violation upper': (violation_upper, get_percentage(len(log), violation_upper)),
			'violation lower': (violation_lower, get_percentage(len(log), violation_lower))}


def check_order(log, first: str, second: str) -> dict:
	"""

	:param log: process log
	:param first:
	:param second:
	:return:
	"""

	violations = 0
	traces = 0

	for trace in log:
		events = trace['events']
		first_stack = []

		if first not in events or second not in events:
			break

		traces += 1

		for event in events:
			if event == first:
				first_stack.append(event)
			elif event == second and len(first_stack) > 0:
				first_stack.pop()
			elif event == second and len(first_stack) == 0:
				violations += 1

	return {'first': first, 'second': second, 'violations': (violations, get_percentage(traces, violations))}


def check_response(log, request: str, response: str) -> dict:
	"""

	:param log:
	:param request: activity which expects a requested activity
	:param response: requested activity
	:return:
	"""

	violations = 0
	traces = 0
	violated_traces = 0

	for trace in log:
		events = trace['events']
		request_stack = []
		trace_contain = True

		for event in events:
			if event == request:
				request_stack.append(event)
				if trace_contain:
					traces += 1
					trace_contain = False

			elif event == response and len(request_stack) > 0:
				request_stack.pop()

		if len(request_stack) > 0:
			violations += len(request_stack)
			violated_traces += 1

	return {'request': request, 'response': response,
			'violations': (violations, traces, violated_traces, get_percentage(traces, violated_traces))}


def check_precedence(log, preceding: str, request: str) -> dict:
	"""

	:param log:
	:param preceding:
	:param request:
	:return:
	"""

	violations = 0

	for trace in log:
		events = trace['events']
		preceding_stack = []

		for event in events:
			if event == preceding:
				preceding_stack.append(event)
			elif event == request and len(preceding_stack) > 0:
				preceding_stack.pop()
			elif event == request and len(preceding_stack) == 0:
				violations += 1

	return {'preceding': preceding, 'request': request, 'violations':
		violations}


def check_exclusive(log, first_activity: str, second_activity: str) -> dict:
	"""

	:param log:
	:param first_activity:
	:param second_activity:
	:return:
	"""

	violations = 0

	for trace in log:
		events = trace['events']

		if first_activity in events and second_activity in events:
			violations += 1

	return {'first activity': first_activity, 'second activity': second_activity,
			'violations': violations}