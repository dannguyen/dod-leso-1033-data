#!/usr/bin/env python
"""
Sample CLI usage:

scripts/compile/clean_agency_name.py "SPRINGFIELD CNTY SHERRIFFS OFFFICE"
"""

from sys import path as syspath; syspath.append('./scripts')
from utils import mylog


from collections import namedtuple
import csv
from pathlib import Path
import re
from sys import argv

AGENCY_PATTERN_FIXES_PATH = Path('data/archived/agency-name-cleanup/agency-pattern-fixes.csv')
agency_pattern_fixes = None

ONEOFFS_PATH = Path('data/archived/agency-name-cleanup/agency-one-off-fixes.csv')
oneoff_names = None

STATE_LOOKUP_PATH = Path('data/archived/crosswalks/us-states.csv')
state_lookups = None

AgencyTuple = namedtuple('AgencyTuple', ('name', 'ctype', 'patterns'))
PatternTuple = namedtuple('PatternTuple', ('pattern', 'match', 'fix', ))



def cleanws(text):
    return re.sub(r'\s+', ' ', str(text)).strip()




def clean_agency_name(name, state):
    global oneoff_names
    oneoff_names = oneoff_names if oneoff_names is not None else ({
            (r['state'], r['original_name']):
              r['fixed_name'] for r in csv.DictReader(open(ONEOFFS_PATH))
            })

    oneoff = oneoff_names.get((state, name,))
    if oneoff:
        name = oneoff
        ctype = 'one-off'
        patterns = ""
    else:
        name, patterns = _clean_agency_name_patterns(name)
        name = _clean_agency_state_abbreviations(name, state)
        ctype = 'regular'

    name = cleanws(name)
    return AgencyTuple(name, ctype, patterns)
#    return namedtuple('agency_name', ('name', 'ctype', 'patterns'))(name, ctype, patterns)


def _clean_agency_name_patterns(name, debug=True):
    """
    test cases:
    JOHNSON CO LAW ENF PROSECUTORS OFF
    """
    global agency_pattern_fixes
    if agency_pattern_fixes is None:
        with open(AGENCY_PATTERN_FIXES_PATH) as src:
            agency_pattern_fixes = list(csv.DictReader(src))

    patterns = None if debug is False else []

    for rx in agency_pattern_fixes:
        mtch = re.search(rx['pattern'], name)
        if mtch:
            name = re.sub(rx['pattern'], rx['fix'], name)
            if debug:
                patterns.append(PatternTuple(rx['pattern'], mtch.group(), rx['fix'],))

    return (name, patterns,)

def _clean_agency_state_abbreviations(name, abbv):
    """if stateabbr appears in name, like SOUTHEAST OH; change it to the full name: SOUTHEAST OHIO """
    global state_lookups
    if state_lookups is None:
       with open(STATE_LOOKUP_PATH) as src:
            state_lookups = {k['usps']: k['name'] for k in csv.DictReader(src)}

    rx = r'\b' + abbv + r'\b'
    if re.search(rx, name) and state_lookups.get(abbv):
        name = re.sub(rx, state_lookups.get(abbv).upper(), name)

    return name



if __name__ == '__main__':
    # if len(state) != 2:
    #     mylog("Warning: the first argument is supposed to be agency name, the second is state abbreviation")
    if len(argv) < 2:
        mylog("Example usage:")
        mylog("""$ clean_agency_name.py "SPRINGFIELD CNTY SHERRIFF'S OFFICE" IA""")
    else:
        name = argv[1]
        state = argv[2] if len(argv) == 3 else "[NONE]"

        mylog(f"Original name: {name}")
        mylog(f"State: {state}")
        mylog(f"")
        for k, v in clean_agency_name(name, state)._asdict().items():
            mylog(f"{k}:\n  {v}")





def _tag_federal(text):
    """
    EPA/USDA/SEC/FEC/USDVA/ATF/NPS/FBI/DOJ
    """
    pass

def _tag_school(text):
    r"""
    HI_ED
    K[_\-]12
    """
    pass
