import os
from pathlib import Path
from pprint import pprint

from conformance_checking.rule_base import Rule_Checker
from util import import_xes_log
# %%
working_dir = Path("C:/Users/Simon.Remy/ownCloud/Projects/BPI19/BPI19 - Logs")

os.chdir(working_dir)
print('changed directory to: %s' % os.getcwd())

log_file = Path("consignment_filtered/consignment without start_end.xes")

log = import_xes_log(log_file)
print('length: %s' % len(log))
print(log[0])

rc = Rule_Checker()
# %%
print('####### precedence rules ########')
res = rc.check_precedence(log, 'Create Purchase Order Item', 'Record Goods Receipt')
pprint(res)

res = rc.check_precedence(log, 'Create Purchase Order Item', 'Record Goods Receipt', True)
pprint(res)
