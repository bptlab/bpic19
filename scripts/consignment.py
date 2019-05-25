import os
from pathlib import Path
from pprint import pprint

from conformance_checking.rule_base import Rule_Checker
from util import import_xes_log
# %%
working_dir = Path("...")

os.chdir(working_dir)
print('changed directory to: %s' % os.getcwd())

log_file = Path("consignment_filtered/consignment without start_end.xes")
log_file_short = str(log_file).split('.xes')[0]

log = import_xes_log(log_file)
print('length: %s' % len(log))
print(log[0])

rc = Rule_Checker()
# %%
print('####### precedence rules ########')
res = rc.check_precedence(log, 'Create Purchase Order Item', 'Record Goods Receipt', file=log_file_short)
pprint(res)
print()
res = rc.check_precedence(log, 'Create Purchase Order Item', 'Record Goods Receipt', True, file=log_file_short)
pprint(res)
