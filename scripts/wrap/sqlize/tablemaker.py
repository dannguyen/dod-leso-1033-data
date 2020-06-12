#!/usr/bin/env python
#

"""
sample usage


    --src data/archived/samples/compiled-state-agencies.sample.csv \


scripts/wrap/sqlize/tablemaker.py \
    --db data/wrapped/db.sqlite \
    --src data/compiled/state-agencies.csv \
    --table 'compiled_agency' \
    --create scripts/wrap/sqlize/schemas/tbl_compiled_agency.sql \
    --index scripts/wrap/sqlize/schemas/idx_compiled_agency.sql \
    --drop


real    0m33.669s
user    0m27.179s
sys 0m5.778s

real    0m38.623s
user    0m29.909s
sys 0m7.515s
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
    conn = get_connex(db)

    if drop:
        stmt = f"DROP TABLE IF EXISTS {table}"
        mylog(stmt)
        conn.cursor().execute(stmt)

    # create the table
    create_path = Path(create) if create else None
    if create_path:
        mylog(f"Reading CREATE statement from: {create_path}")
        stmt = create_path.read_text()
    else:
        stmt = derive_create_stmt(src, table)
    mylog(stmt)
    conn.cursor().execute(stmt)

    # load the data
    load_bulk_data(conn, src, table)

    # optional indexing
    index_path = Path(index) if index else None
    if index_path:
        mylog(f"Indexing with: {index_path}")
        stmt = index_path.read_text()
        mylog(stmt)
        conn.cursor().execute(stmt)


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
    return connection
#    cursor=connection.cursor()

#    return namedtuple('Connex', ['connection', 'cursor'])(connection, cursor)

def load_bulk_data(conn, srcpath, tablename):
    with open(srcpath) as src:
        data = list(csv.reader(src))

    fields = data[0]
    records = data[1:]

    fieldstr = ', '.join(fields)
    valstr = ', '.join('?' for k in fields)
    querystr = f"INSERT INTO {tablename}({fieldstr}) VALUES ({valstr})"
    mylog(querystr)


    # https://rogerbinns.github.io/apsw/tips.html#write-ahead-logging
    # add write-ahead logging for performance
    # conn.cursor().execute("pragma journal_mode=wal")
    # custom auto checkpoint interval (use zero to disable)

    with conn as db:

        db.cursor().executemany(querystr, records)

if __name__ == '__main__':
    build()
