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
    resFile = './result/result_evitar_{}.csv'.format(2)
    txF.writeTx(w3, resFile, 13)
