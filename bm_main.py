import _thread
import csv
import math
import os
import random
import time

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.replayTx as rTx
import src.txFunction as txF

# MAIN!!


if __name__ == "__main__":
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    w3_2 = Web3(HTTPProvider('http://localhost:8544'))
    csv.field_size_limit(100000000)

    file = sys.argv[1]

    # files = os.listdir("./evitar_tx_by_hash")
    # files.sort()
    # print(files)

    # for file in files:
    fileName = "./evitar_tx_by_hash/"+file
    rTx.replayBaseLineAndMaxGas(w3, w3_2, fileName)

    txF.writeTx(w3, './result/result_baseline_{}.csv'.format{file}, 28)
    txF.writeTx(w3, './result/result_maxgas_{}.csv'.format{file}, 28)
