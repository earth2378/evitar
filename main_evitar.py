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
    evitar = int(sys.argv[2])
    if(evitar == 1):
        thresh = 0.5
        wnd = 50
    elif(evitar == 2):
        thresh = 0.25
        wnd = 50
    elif(evitar == 3):
        thresh = 0.5
        wnd = 10

    directory = "./evitar_tx_by_hash/"
    fileName = "./evitar_tx_by_hash/"+file
    resFile = './result/result_evitar{}_{}'.format(evitar, file)
    # print(fileName)
    # print(resFile)

    rTx.replayEvitar(w3, fileName, thresh, wnd)
    txF.writeTx(w3, './result/result_evitar.csv', 28)
