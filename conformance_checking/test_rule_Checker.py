from unittest import TestCase

from conformance_checking.rule_base import Rule_Checker


class TestRule_Checker(TestCase):

	def setUp(self):
		self.rc = Rule_Checker()
		self.log = [
				{'trace': 1, 'events': ['A', 'B', 'D', 'C', 'E']},
				{'trace': 2, 'events': ['A', 'B', 'D', 'B', 'F']},
				{'trace': 3, 'events': ['B', 'C', 'E']},
				{'trace': 1, 'events': ['B', 'E']}
			]

	def test_get_percentage(self):
		res = self.rc.get_percentage(450, 20)
		self.assertEqual(round(res, 2), 4.44)

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
		self.assertEqual(res['violations'], (2, 1, 25.0))

		res = self.rc.check_response(self.log, 'A', 'D')
		self.assertEqual(res['violations'], (0, 0, 0.0))

	def test_check_precedence(self):
		res = self.rc.check_precedence(self.log, 'B', 'C')
		self.assertEqual(res['violations'], (0, 0, 0.0))

	def test_check_exclusive(self):
		res = self.rc.check_exclusive(self.log, 'E', 'F')
		self.assertEqual(res['violations'][0], 0)

		res = self.rc.check_exclusive(self.log, 'A', 'B')
		self.assertEqual(res['violations'][0], 2)

