import os
from pathlib import Path
from pprint import pprint

from conformance_checking.rule_base import Rule_Checker
from util import import_xes_log
# %%
working_dir = Path("C:/Users/Simon.Remy/ownCloud/Projects/BPI19/BPI19 - Logs")

os.chdir(working_dir)
print('changed directory to: %s' % os.getcwd())

log_file = Path("Invoice before GR (Standard).xes")

log = import_xes_log(log_file, '{http://www.xes-standard.org}')
print('length: %s' % len(log))
print(log[0])

rc = Rule_Checker()
# %%
print('####### order rules ########')
res = rc.check_order(log, 'Remove Payment Block', 'Clear Invoice')
pprint(res)
print()

res = rc.check_order(log, 'Change Quantity', 'Record Invoice Receipt')
pprint(res)
print()

res = rc.check_order(log, 'Change Quantity', 'Record Goods Receipt')
pprint(res)
print()

# %%
print('####### response rules ########')
res = rc.check_response(log, 'Create Purchase Requisition Item', 'Create Purchase Order Item')
pprint(res)
print()

res = rc.check_response(log, 'Record Goods Receipt', 'Record Invoice Receipt')
pprint(res)
print()

res = rc.check_response(log, 'Record Invoice Receipt', 'Clear Invoice')
pprint(res)
print()

res = rc.check_response(log, 'Record Invoice Receipt', 'Clear Invoice', True)
pprint(res)
print()

# %%
print('####### precedence rules ########')
res = rc.check_precedence(log, 'Record Invoice Receipt', 'Clear Invoice')
pprint(res)
print()

res = rc.check_precedence(log, 'Record Goods Receipt', 'Clear Invoice')
pprint(res)
print()

res = rc.check_precedence(log, 'Set Payment Block', 'Remove Payment Block')
pprint(res)
print()

# %%
print('####### cardinality rules ########')
res = rc.check_cardinality(log, 'Create Purchase Order Item', 1, 1)
pprint(res)
print()

res = rc.check_cardinality(log, 'Change Price', 1, 0)
pprint(res)
print()

res = rc.check_cardinality(log, 'Change Quantity', 1, 0)
pprint(res)
print()

res = rc.check_cardinality(log, 'Record Goods Receipt', 1, 1)
pprint(res)
print()

res = rc.check_cardinality(log, 'Record Invoice Receipt', 1, 1)
pprint(res)
print()

res = rc.check_cardinality(log, 'Clear Invoice', 1, 1)
pprint(res)
print()

res = rc.check_cardinality(log, 'Vendor creates invoice', 1, 1)
pprint(res)
print()

# %%
print('####### exclusive rules ########')
res = rc.check_exclusive(log, 'Receive Order Confirmation', 'Clear Price')
pprint(res)
