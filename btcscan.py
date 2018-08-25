import json
from logging import warning

import requests


def btcscan_io(pages):
    idx = requests.get('https://blockexplorer.com/api/status?q=getBlockCount').json().get('blockcount')
    if not idx:
        return []

    hashes = [
        requests.get('https://blockexplorer.com/api/block-index/{}'.format(idx - i)).json().get('blockHash')
        for i in range(0, pages)
    ]

    pattern = 'https://blockexplorer.com/api/txs?block={}'

    warning('HASHES %s', hashes)
    return [pattern.format(h) for h in hashes]


def btc_valid(obj):
    return obj['from'] is not None


def first_input(tx):
    ins = tx.get('vin', [])
    if len(ins) == 0:
        warning('Empty %s', tx)
        return None
    if len(ins) > 1:
        # print("skipping ", ins)
        return None
    return next(iter(ins), {}).get('addr')


def sum_val(tx):
    return tx.get('valueOut', 0)


def btcscan_to_obj(data):
    data = json.loads(data)
    return [{ 'tx_id': d.get('txid'), 'from': first_input(d), 'to': None, 'value': sum_val(d)}
            for d in data.get('txs')]
