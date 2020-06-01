#!/usr/bin/env python

"""
collect.py

Reads data_manifest.yaml, and for each "data/collected" entry, downloads from the
  corresponding `url`

"""
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

        stderr.write(f"\n{dest_path}\n")
        if dest_path.is_file() and dest_path.stat().st_size > 1023:
            stderr.write(f'\talready exists: {dest_path.stat().st_size} bytes\n')
        else:
            stderr.write(f"\tDownloading: {url}\n")

            content = fetch_file(url)

            dest_path.parent.mkdir(exist_ok=True, parents=True)
            dest_path.write_bytes(content)

            stderr.write(f"\tWrote {len(content)} bytes\n")


if __name__ == '__main__':
    main()
