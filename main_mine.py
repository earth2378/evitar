import _thread
import csv
import math
import os
import random
import time

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.replayTx as rTx
import src.txFunction as txF

if __name__ == "__main__":
    port = sys.argv[1]
    w3 = Web3(HTTPProvider('http://localhost:'+port))
    counter = 0
    while(true):
        pendingTx = int(w3.geth.txpool.status()['pending'],0)
        if(counter == 10):
            break
        if(pendingTx > 1000):
            counter = 0
            txF.minePendingTx(w3,1)
        count += 1

        time.sleep(5)

