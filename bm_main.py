import _thread
import csv
import math
import os
import random
import sys
import time

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.replayTx as rTx
import src.txFunction as txF

# MAIN!!


if __name__ == "__main__":
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    # w3_2 = Web3(HTTPProvider('http://localhost:8544'))
    csv.field_size_limit(100000000)

    mode = sys.argv[1]

    low_mem = ['0x0.csv','0x3.csv','0x4.csv','0x5.csv','0x6.csv','0x7.csv','0x9.csv','0xa.csv','0xb.csv','0xc.csv','0xd.csv','0xe.csv','0xf.csv']
    high_mem = ['0x1.csv','0x2.csv','0x8.csv']

    if mode == 'low_mem':
        for file in low_mem:
            print(file)
            fileName = "./evitar_tx_by_hash/"+file
            rTx.replayBaseLineAndMaxGas(w3, w3_2, fileName)
    elif mode == 'high_mem':
        for file in high_mem:
            print(file)
            fileName = "./evitar_tx_by_hash/"+file
            rTx.replayBaseLineAndMaxGas(w3, w3_2, fileName)
    else:
        print('low_mem or high_mem only')

