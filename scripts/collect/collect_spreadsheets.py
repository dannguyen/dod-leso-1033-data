#!/usr/bin/env python

"""
collect.py

Reads data_manifest.yaml, and for each "data/collected" entry, downloads from the
  corresponding `url`
"""
from sys import path as syspath; syspath.append('./scripts')
from utils import mylog

from pathlib import Path
import requests
from sys import stderr
import yaml


INVENTORY_PATH = Path('data_inventory.yaml')

def collect_inventory():
    """
    returns list of tuples, with file filepath and source url

    filtered for data/collected prefixes
    """
    mani = yaml.load(INVENTORY_PATH.open(), Loader=yaml.BaseLoader)
    return [(filepath, v['url']) for filepath, v in mani.items() if 'data/collected' in filepath]


def fetch_file(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        # be noisy and alert the user that the download unexpectedly failed
        raise ValueError(f"Got status code {resp.status_code} for: {url}")
    return resp.content



def main():
    for filename, url in collect_inventory():
        dest_path = Path(filename)

        mylog(f"\n{dest_path}")
        if dest_path.is_file() and dest_path.stat().st_size > 1023:
            mylog(f'\talready exists: {dest_path.stat().st_size} bytes')
        else:
            mylog(f"\tDownloading: {url}")

            content = fetch_file(url)

            dest_path.parent.mkdir(exist_ok=True, parents=True)
            dest_path.write_bytes(content)

            mylog(f"\tWrote {len(content)} bytes")


if __name__ == '__main__':
    main()
