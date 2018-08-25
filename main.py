import json
from logging import warning

import requests
import argparse

import sys

from btcscan import btcscan_io, btcscan_to_obj, btc_valid
from ethscan import ethscan_io, ethscan_to_obj, eth_valid

UrlLoader = {
    'eth': ethscan_io,
    'btc': btcscan_io,
}

UrlParsers = {
    'eth': ethscan_to_obj,
    'btc': btcscan_to_obj,
}

IsValid = {
    'eth': eth_valid,
    'btc': btc_valid,
}


def main(args):
    parser = argparse.ArgumentParser(args)
    parser.add_argument('type', help='Scanner type')
    parser.add_argument('pages', help='Pages', type=int)
    args = parser.parse_args()

    all_objs = []
    for url in UrlLoader[args.type](args.pages):
        warning('reqing %s', url)
        data = requests.get(url, verify=False).text
        objects = UrlParsers[args.type](data)
        for obj in objects:
            if obj and IsValid[args.type](obj) and obj['value'] > 0.5:
                all_objs.append(obj)
    print(json.dumps(all_objs))


if __name__ == '__main__':
    main(sys.argv)
