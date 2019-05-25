# Business Process Intelligence Challenge 19 - Rule Checker
This Python package can be used to specify and check control-flow based business rules for event logs.

## Existing Scripts
The directory `scripts/` contains ready-to-run scripts, to check predefined rules for different item-types, as described in the report.

## Examples

### Import XES log
Follow the steps below, to import an XES event log:
````
form util import import_xes_log

path_to_log = './event_log.xes')
log = import_xes_log(path_to_log)
````
Beside the activity names, only certain, BPIC19 specific case attributes, will be imported.

### Define and Check Rules
Follow the steps below, to define and check business rules.
````
from conformance_checking.rule_base import Rule_Checker
from pprint import pprint

rc = Rule_Checker()
res = rc.check_response(log, 'Vendor creates invoice', 'Record Invoice Receipt')
pprint(res)
````
The `check_precedence()` function takes a path value as additional argument in order to export the `case ID` and other case attributes of violated cases. 

