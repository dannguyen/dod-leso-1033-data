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
SRCDATE_DIRS = sorted(SRC_DIR.glob('*/all-states'))
DEST_DIR = Path('data/compiled/state-agencies')
DEST_PATH_ALL = DEST_DIR.joinpath('ALL.csv')
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

def load_sheet_csv(srcpath):
    """
    Returns: <list> of dicts
    """
    meta = metasize_csvpath(srcpath)
    data = []
    with open(srcpath) as src:
        for row in csv.DictReader(src):
            d = meta.copy()
            for h, val in row.items():
                newh = HEADER_MAP[h]
                d[newh] = cleanws(row[h])
                if newh == 'ship_date':
                    d['org_ship_date'] = d['ship_date']
                    d['ship_date'] = d['org_ship_date'][:10]
            data.append(d)


    metatxt = f"{meta['file_date']}/{meta['book_name']}/{meta['sheet_name']}"
    mylog(f"{metatxt}:".ljust(50) + f" {len(data)} rows")

    return data

def write_compiled_date_csv(data, destdir, file_date,):
    destpath = destdir.joinpath(f'{file_date}.csv')
    with open(destpath, 'w') as dest:
        outs = csv.DictWriter(dest, fieldnames=COMPILED_HEADERS)
        outs.writeheader()
        outs.writerows(data)
    mylog(f"Wrote {len(data)} rows to: {destpath}")




def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    mylog(f"Found {len(SRCDATE_DIRS)} date directories")

    alldest = open(DEST_PATH_ALL, 'w')
    allouts = csv.DictWriter(alldest, fieldnames=COMPILED_HEADERS)
    allouts.writeheader()

    for datedir in SRCDATE_DIRS:
        sheetpaths = sorted(datedir.glob('*.csv'))
        mylog(f"{datedir}: {len(sheetpaths)} csv files")


        # each datedir looks like:
        # data/collected/disp/agencies/2019-12-31/all-states
        filedate = datedir.parent.name

        datedata = []
        for sheetpath in sheetpaths:
            sdata = load_sheet_csv(sheetpath)
            datedata.extend(sdata)
        write_compiled_date_csv(datedata, DEST_DIR, filedate)
        allouts.writerows(datedata)

    mylog("-30-")
    mylog(f"Wrote all rows into: {DEST_PATH_ALL}")
    alldest.close()
    # for srcpath in srcpaths:
    #     data = load_csv(srcpath)

    #     meta = metasize_csvpath(srcpath)

    #     outs.writerows(data)

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
