from unittest import TestCase
from io import import_xes_log

class TestImport_xes_log(TestCase):
	def test_import_xes_log(self):
		log = import_xes_log("./notebooks/Invoice after GR (with EC, wo start "
							 "and end).xes")

