"""

"""

import pandas as pd
import xml.etree.ElementTree as xmlTree


def import_csv_log(file: str):
	return pd.read_csv(file)


def import_xes_log(file, prefix=''):
	log = []

	tree = xmlTree.parse(file)
	root = tree.getroot()
	# find all traces
	print(root)
	traces = root.findall(''.join([prefix, 'trace']))

	for t in traces:
		trace_id = None

		# get trace id
		for a in t.findall(''.join([prefix, 'string'])):
			if a.attrib['key'] == 'concept:name':
				trace_id = a.attrib['value']

		events = []
		# events
		for event in t.iter(''.join([prefix, 'event'])):
			for a in event:
				if a.attrib['key'] == 'concept:name':
					events.append(a.attrib['value'])

		log.append({'trace_id': trace_id, 'events': events})

	print('Found %s traces' % (len(traces)))
	return log
