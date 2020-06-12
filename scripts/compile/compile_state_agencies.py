#!/usr/bin/env python

"""
Differences between collected and compiled data:
- standardized header names
- ship_date is just date, not datetime
- whitespace squeezed and stripped (cleanws(text))

"""

from sys import path as syspath; syspath.append('./scripts')
from utils import mylog
import csv
from pathlib import Path
import re
from sys import stdout

SRC_DIR = Path('data/collected/disp/agencies')
# DEST_PATH = Path('data/compiled/state-agencies.csv')

HEADER_MAP = {
    'State': 'state',
    'Station Name (LEA)': 'station_name',
    'NSN': 'nsn',
    'Item Name': 'item_name',
    'Quantity': 'quantity',
    'UI': 'ui',
    'Acquisition Value': 'acquisition_value',
    'DEMIL Code': 'demil_code',
    'DEMIL IC': 'demil_ic',
    'Ship Date': 'ship_date',
    'Station Type': 'station_type',
}

COMPILED_HEADERS = list(HEADER_MAP.values()) + ['org_ship_date', 'file_date', 'book_name', 'sheet_name']


def cleanws(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def metasize_csvpath(fullpath):
    """
    fullpath <str> or <Path>
        e.g. 'data/collected/disp/agencies/2020-03-31/all-states/Alabama.csv'

    Returns: <dict>
    {
        'file_date': '2020-03-31',
        'book_name': 'all-states',
        'sheet_name': 'Alabama',
    }
    """
    path = Path(fullpath)
    d = {}
    d['file_date'] = path.parent.parent.name
    d['book_name'] = path.parent.name
    d['sheet_name'] = path.stem
    return d

def gather_csvs():
    return sorted(SRC_DIR.rglob('*states*/*.csv'))


def load_csv(srcpath):
    """
    Returns: <list> of dicts
    """
    metainfo = metasize_csvpath(srcpath)

    data = []
    with open(srcpath) as src:
        for row in csv.DictReader(src):
            d = metainfo.copy()
            for h, val in row.items():
                newh = HEADER_MAP[h]
                d[newh] = cleanws(row[h])
                if newh == 'ship_date':
                    d['org_ship_date'] = d['ship_date']
                    d['ship_date'] = d['org_ship_date'][:10]
            data.append(d)
    return data


def main():
    srcpaths = gather_csvs()
    mylog(f"Found {len(srcpaths)} csv files")

    outfile = stdout
    outs = csv.DictWriter(outfile, fieldnames=COMPILED_HEADERS)
    outs.writeheader()

    for srcpath in srcpaths:
        meta = metasize_csvpath(srcpath)
        metainfo = f"{meta['file_date']}/{meta['book_name']}/{meta['sheet_name']}"

        data = load_csv(srcpath)
        mylog(f"{metainfo}:\t {len(data)} rows")

        outs.writerows(data)

if __name__ == '__main__':
    main()


"""
The different formats:

2016-04-04 through 2019-09-30: 10 headers

    1   State
    2   Station Name (LEA)
    3   NSN
    4   Item Name
    5   Quantity
    6   UI
    7   Acquisition Value
    8   DEMIL Code
    9   DEMIL IC
    10  Ship Date

2019-12-31 on forward: 11 headers

    1   State
    2   Station Name (LEA)
    3   NSN
    4   Item Name
    5   Quantity
    6   UI
    7   Acquisition Value
    8   DEMIL Code
    9   DEMIL IC
    10  Ship Date
    11  Station Type
"""
