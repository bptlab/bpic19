from unittest import TestCase

from conformance_checking.rule_base import Rule_Checker


class TestRule_Checker(TestCase):

	def setUp(self):
		self.rc = Rule_Checker()
		self.log = [
				{'trace': 1, 'events': ['A', 'B', 'D', 'C', 'E']},
				{'trace': 2, 'events': ['A', 'B', 'D', 'B', 'F']},
				{'trace': 3, 'events': ['B', 'C', 'E']},
				{'trace': 1, 'events': ['B', 'E']},
				{'trace': 1,
				 'events': ['A', 'B', 'C', 'E', 'C', 'D']}, # single pre
				{'trace': 1, 'events': ['A', 'C', 'B', 'E', 'C', 'D']},
				{'trace': 1, 'events': ['G', 'G', 'E', 'T', 'G']},
			]

	def test_get_percentage(self):
		res = self.rc.get_percentage(450, 20)
		self.assertEqual(res, 4.44)

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
		res = self.rc.check_precedence(self.log, 'B', 'C')
		self.assertEqual(res['violations'], (2, 2, 50.0))

		res = self.rc.check_precedence(self.log, 'B', 'C', True)
		self.assertEqual(res['violations'], (1, 1, 25.0))

	def test_check_exclusive(self):
		res = self.rc.check_exclusive(self.log, 'E', 'F')
		self.assertEqual(res['violations'][0], 0)

		res = self.rc.check_exclusive(self.log, 'A', 'B')
		self.assertEqual(res['violations'][0], 2)

