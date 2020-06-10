#!/usr/bin/env python
#

"""
sample usage

scripts/wrap/sqlize/tablemaker.py \
    --db data/wrapped/db.sqlite \
    --src data/archived/samples/compiled-state-agencies.sample.csv \
    --table 'compiled_agency' \
    --create scripts/wrap/sqlize/schemas/tbl_compiled_agency.sql \
    --index scripts/wrap/sqlize/schemas/idx_compiled_agency.sql \
    --drop


"""
from sys import path as syspath; syspath.append('./scripts')
from utils import mylog


import apsw
import click
from collections import namedtuple
import csv
from pathlib import Path



@click.command()
@click.option('--db', required=True, type=click.Path())
@click.option('--src', required=True,  type=click.Path(exists=True, readable=True))
@click.option('--table', required=True,   type=click.STRING)
@click.option('--create', type=click.Path(exists=True), help='path to CREATE sql file')
@click.option('--index',  type=click.Path(exists=True), help='path to indexing sql file')
@click.option('--drop/--no-drop', default=False, help='if true, then `drop <tablename>`')

def build(db, src, table, create, index, drop):
    cx = get_connex(db)

    if drop:
        stmt = f"DROP TABLE IF EXISTS {table}"
        mylog(stmt)
        cx.cursor.execute(stmt)

    # create the table
    create_path = Path(create) if create else None
    if create_path:
        mylog(f"Reading CREATE statement from: {create_path}")
        stmt = create_path.read_text()
    else:
        stmt = derive_create_stmt(src, table)
    mylog(stmt)
    cx.cursor.execute(stmt)

    # load the data
    load_bulk_data(cx.cursor, src, table)

    # optional indexing
    index_path = Path(index) if index else None
    if index_path:
        mylog(f"Indexing with: {index_path}")
        stmt = create_path.read_text()
        mylog(stmt)
        cx.cursor.execute(stmt)


def derive_create_stmt(srcpath, tablename):
    # read first line (i.e. headers) and generate a simple CREATE statement
    with open(srcpath, 'r') as src:
        inx = csv.reader(src)
        headers = next(inx)
    txt = f"""CREATE TABLE IF NOT EXISTS {tablename}({', '.join(f'"{h}"' for h in headers)});""".strip()
    return txt

def get_connex(db_path):
    dbpath = Path(db_path).expanduser().as_posix()
    connection = apsw.Connection(dbpath)
    cursor=connection.cursor()

    return namedtuple('Connex', ['connection', 'cursor'])(connection, cursor)

def load_bulk_data(cursor, srcpath, tablename):
    with open(srcpath) as src:
        data = list(csv.reader(src))

    fields = data[0]
    records = data[1:]

    fieldstr = ', '.join(fields)
    valstr = ', '.join('?' for k in fields)
    querystr = f"INSERT INTO {tablename}({fieldstr}) VALUES ({valstr})"
    mylog(querystr)
    cursor.executemany(querystr, records)


# def main():
#     cx = get_connex(TEST_DB_PATH)
#     cx.cursor.execute(CREATE_STMT)
#     load_bulk_data(cx.cursor, TEST_SRC_PATH, 'compiled_state_agency')

if __name__ == '__main__':
    build()
