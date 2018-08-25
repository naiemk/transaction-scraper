from logging import warning

from bs4 import BeautifulSoup as Soup
from soupselect import select


def ethscan_io(pages):
    return ['https://etherscan.io/txs?p={}'.format(i) for i in range(1, pages + 1)]


def ethscan_to_obj(data):
    html = Soup(data)
    body = select(html, 'tbody')[0]
    trs = select(body, 'tr')
    for tr in trs:
        yield parse_row(tr)


def eth_valid(obj):
    return obj['from'] and obj['to']


def strip(adrs):
    if not adrs:
        return adrs
    if adrs.startswith('0x'):
        return adrs[2:]
    return None


def parse_row(tr):
    if not tr:
        return None
    address = select(tr, '.address-tag a')
    if len(address) != 3:
        warning(tr)
        return None
    tx_id = address[0].contents[0]
    tx_from = address[1].contents[0]
    tx_to = address[2].contents[0]
    tds = select(tr, 'td')
    val = tds[6].text
    num_val = float(val.replace('Ether', '').replace(' ', '')) if 'Ether' in val else 0
    return {
        'tx_id': strip(tx_id),
        'from': strip(tx_from),
        'to': strip(tx_to),
        'value': num_val
    }
