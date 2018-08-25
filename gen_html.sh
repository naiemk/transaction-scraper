#!/bin/bash

python ./main.py eth 20 > dnlds/eth.txt
python ./main.py btc 30 > dnlds/btc.txt

export BTC_TRANS=$(cat dnlds/btc.txt)
export ETH_TRANS='[]'

bash trans.html.template > out/transbtc.html

export BTC_TRANS='[]'
export ETH_TRANS=$(cat dnlds/eth.txt)

bash trans.html.template > out/transeth.html

