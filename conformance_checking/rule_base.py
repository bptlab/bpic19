class Rule_Checker():

	def get_percentage(self, total: int, observations: int) -> float:
		return round((100 / total) * observations, 2)

	def check_cardinality(self, log, activity: str, upper: int, lower: int) \
			-> \
			dict:
		"""

		:param log: event log
		:param activity: name of the activity
		:param upper: max. number of occurrence in one trace, -1 if infinite
		:param lower: min. number of occurrence in one trace
		:return: report
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
				'violation upper': (violation_upper,
									self.get_percentage(len(log),
														violation_upper)),
				'violation lower': (violation_lower,
									self.get_percentage(len(log),
														violation_lower))}

	def check_order(self, log, first: str, second: str) -> dict:
		"""

		:param log: event log
		:param first: activity
		:param second: activity
		:return: report
		"""

		violations = 0
		traces = 0

		for trace in log:
			events = trace['events']
			first_stack = []

			if first in events and second in events:
				traces += 1

				for event in events:
					if event == first:
						first_stack.append(event)
					elif event == second and len(first_stack) == 0:
						violations += 1

		return {'first': first, 'second': second,
				'violations': (violations,
							   self.get_percentage(traces, violations))}

	def check_response(self, log, request: str, response: str,
					   single_occurrence=False) -> dict:
		"""

		:param log: event log
		:param request: activity which expects a requested activity
		:param response: requested activity
		:param single_occurrence: specifies whether a single occurrence of the
		responding activity already satisfies the rule
		:return: report
		"""

		violations = 0
		traces = 0
		violated_traces = 0

		for trace in log:
			events = trace['events']
			req_stack = []

			tracked = False

			if not single_occurrence:
				for event in events:
					if event == request:
						req_stack.append(event)
						if not tracked:
							traces += 1
							tracked = True
					elif event == response and len(req_stack) > 0:
						req_stack.pop()

				if len(req_stack) > 0:
					violations += len(req_stack)
					violated_traces += 1
			else:
				if request in events and response in events:
					traces += 1
					req_idx = events[::-1].index(request)
					res_idx = events[::-1].index(response)

					if req_idx < res_idx:
						violations += 1
						violated_traces += 1
				elif request in events and response not in events:
					traces += 1
					violated_traces += 1
					violations += 1

		return {'request': request, 'response': response,
			'violations': (violations, violated_traces,
						   self.get_percentage(traces, violated_traces)),
				'single': single_occurrence}

	def check_precedence(self, log, preceding: str, request: str,
						 single_occurrence=False) -> dict:
		"""

		:param log: event log
		:param preceding: activity that should precede the requesting activity
		:param request: requesting activity
		:param single_occurrence: specifies whether a single occurrence of the
		preceding activity already satisfies the rule
		:return: report
		"""

		violations = 0
		traces = 0
		violated_traces = 0

		for trace in log:
			events = trace['events']
			pre_stack = []

			tracked = False
			violated_trace_tracked = False

			for event in events:
				if event == preceding:
					pre_stack.append(event)
				elif event == request and len(pre_stack) > 0:
					if not single_occurrence:
						pre_stack.pop()
					if not tracked:
						traces += 1
						tracked = True
				elif event == request:
					violations += 1
					if not violated_trace_tracked:
						violated_traces += 1
						violated_trace_tracked = True
					if not tracked:
						traces += 1
						tracked = True

		return {'preceding': preceding, 'request': request,
				'violations': (violations, violated_traces,
							   self.get_percentage(traces, violated_traces)),
				'single': single_occurrence}

	def check_exclusive(self, log, first_activity: str, second_activity: str) \
			-> dict:
		"""

		:param log: event log
		:param first_activity: activity
		:param second_activity: activity
		:return: report
		"""

		violations = 0
		violated_traces = 0

		for trace in log:
			events = trace['events']

			if first_activity in events and second_activity in events:
				violated_traces += 1
				violations += 1

		return {'first activity': first_activity,
				'second activity': second_activity,
				'violations': (violations,
							   self.get_percentage(len(log), violated_traces))}
