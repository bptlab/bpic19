import os
from pathlib import Path
from pprint import pprint

from conformance_checking.rule_base import Rule_Checker
from util import import_xes_log
# %%
working_dir = Path("C:/Users/Simon.Remy/ownCloud/Projects/BPI19/BPI19 - Logs")

os.chdir(working_dir)
print('changed directory to: %s' % os.getcwd())

log_file = Path("2-way matching_filtered/2-way matching (without changeApprovalforPO).xes")

log = import_xes_log(log_file)
print('length: %s' % len(log))
print(log[0])

rc = Rule_Checker()
# %%
print('####### response rules ########')
res = rc.check_response(log, 'Vendor creates invoice', 'Record Invoice Receipt')
pprint(res)

res = rc.check_response(log, 'Record Invoice Receipt', 'Clear Invoice')
pprint(res)

print('####### precedence rules ########')
res = rc.check_precedence(log, 'Record Invoice Receipt', 'Clear Invoice')
pprint(res)
