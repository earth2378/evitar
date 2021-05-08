import _thread
import csv
import math
import os
import random
import time, sys

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.replayTx as rTx
import src.txFunction as txF

if __name__ == "__main__":
    port = sys.argv[1]
    w3 = Web3(HTTPProvider('http://localhost:'+port))
    counter = 0
    pendingTx = 0

    print("Waiting for initialization.")

    while(pendingTx == 0):
        pendingTx = int(w3.geth.txpool.status()['pending'],0)
        time.sleep(5)

    print("Initialize complete.")

    while(True):
        pendingTx = int(w3.geth.txpool.status()['pending'],0)
        # 5 min
        if(counter == 60):
            break
        if(pendingTx > 2000):
            print("Start mining ...")
            counter = 0
            txF.minePendingTxWithThresh(w3,2,500)
            print("Pause mining ...")
        counter += 1

        time.sleep(5)

    txF.minePendingTx(w3,2)
    print("Finished")

    

