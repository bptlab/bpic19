from unittest import TestCase

from conformance_checking.rule_base import Rule_Checker


class TestRule_Checker(TestCase):

	def setUp(self):
		self.rc = Rule_Checker()
		self.log = [
				{'trace': 1, 'events': ['A', 'B', 'D', 'C', 'E']},
				{'trace': 2, 'events': ['A', 'B', 'D', 'B', 'F']},
				{'trace': 3, 'events': ['B', 'C', 'E']},
				{'trace': 4, 'events': ['B', 'E']},
				{'trace': 5,
				 'events': ['A', 'B', 'C', 'E', 'C', 'D']}, # single pre
				{'trace': 6, 'events': ['A', 'C', 'B', 'E', 'C', 'D']},
				{'trace': 7, 'events': ['G', 'G', 'E', 'T', 'G']},
			]

	def test_get_percentage(self):
		res = self.rc.get_percentage(450, 20)
		self.assertEqual(res, 4.44)

	def test_export_case_ids(self):
		ids = ['123', '456', '789']
		self.rc.export_case_ids('test_ids.txt', ids)

	def test_check_cardinality(self):
		res = self.rc.check_cardinality(self.log, 'A', 1, 0)

		self.assertEqual(res['violation upper'][0], 0)
		self.assertEqual(res['violation lower'][0], 0)

		res = self.rc.check_cardinality(self.log, 'B', 1, -1)
		self.assertEqual(res['violation upper'][0], 1)
		self.assertEqual(res['violation lower'][0], 0)

	def test_check_order(self):
		res = self.rc.check_order(self.log, 'A', 'B')
		self.assertEqual(res['violations'][0], 0)

	def test_check_response(self):
		res = self.rc.check_response(self.log, 'B', 'E')
		self.assertEqual(res['violations'], (2, 1, 16.67))

		res = self.rc.check_response(self.log, 'A', 'D')
		self.assertEqual(res['violations'], (0, 0, 0.0))

		res = self.rc.check_response(self.log, 'G', 'T', True)
		self.assertEqual(res['violations'], (1, 1, 100.0))

		res = self.rc.check_response(self.log, 'G', 'T')
		self.assertEqual(res['violations'], (2, 1, 100.0))

	def test_check_precedence(self):

		log = [
			{'trace_id': '1', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a', 'events': ['A', 'B']},
			{'trace_id': '2', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a', 'events': ['A', 'B', 'R']}, # fail 1
			{'trace_id': '3', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a', 'events': ['A', 'P', 'B', 'R']}, #t
			{'trace_id': '4', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a', 'events': ['A', 'R', 'B', 'P']}, # fail 1
			{'trace_id': '5', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a', 'events': ['A', 'P', 'B', 'P', 'R']}, # t
			{'trace_id': '6', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'R', 'R']}, # fail 1
			{'trace_id': '7', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'P', 'R', 'R']}, # t
			{'trace_id': '8',  'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P']},
			{'trace_id': '9',  'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'R', 'P', 'R', 'P']}, # fail 1
			{'trace_id': '10', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'R', 'R']} # fail 2
		]

		res = self.rc.check_precedence(log, 'P', 'R')
		self.assertEqual(res['violations'], (6, 5, 62.5))

	def test_check_precedence_single(self):

		log = [
			{'trace_id': '1', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'B']},
			{'trace_id': '2', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'B', 'R']},  # fail 1
			{'trace_id': '3', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'R']},  # t
			{'trace_id': '4', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'R', 'B', 'P']},  # fail 1
			{'trace_id': '5', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'P', 'R']},  # t
			{'trace_id': '6', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'R', 'R']},  # t
			{'trace_id': '7', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P', 'B', 'P', 'R', 'R']},  # t
			{'trace_id': '8', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'P']},
			{'trace_id': '9', 'vendor': 'A', 'value': 'a', 'spend_area': 'a', 'item_type': 'a','events': ['A', 'R', 'P', 'R', 'P']}  # fail 1
		]

		res = self.rc.check_precedence(log, 'P', 'R', True)
		self.assertEqual(res['violations'], (3, 3, 42.86))

	def test_check_exclusive(self):
		res = self.rc.check_exclusive(self.log, 'E', 'F')
		self.assertEqual(res['violations'][0], 0)

		res = self.rc.check_exclusive(self.log, 'A', 'B')
		self.assertEqual(res['violations'][0], 4)

