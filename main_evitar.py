import _thread
import csv
import math
import os
import random
import sys
import time

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.initNode as init
import src.replayTx as rTx
import src.txFunction as txF

# MAIN!!
if __name__ == "__main__":

    w3 = Web3(HTTPProvider('http://localhost:8545'))
    file = sys.argv[1]
    thresh = float(sys.argv[2])
    wnd = int(sys.argv[3])
    directory = "./evitar_tx_by_hash/"

    # files = os.listdir("./evitar_tx_by_hash")
    # files.sort()
    # print(files)

    # for file in files:
    fileName = "./evitar_tx_by_hash/"+file
    rTx.replayEvitar(w3, fileName, thresh, wnd)

    print(fileName)
    resFile = './result/result_{}_{}_{}'.format(thresh, str(wnd), file)
    print(resFile)
    txF.writeTx(w3, './result/result_evitar.csv', 28)
