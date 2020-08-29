import math,csv,time,_thread,os,random
import src.txFunction as txF
import src.initNode as init
import src.replayTx as rTx
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

# MAIN!!


if __name__ == "__main__":

    thresh = 0.9
    wnd = 0.2
    directory = "./evitar_tx_by_hash/"

    fileList = os.listdir("./evitar_tx_by_hash")
    fileList.sort()
    print(fileList)
    for file in fileList:
        fileName = directory + file
        with open(fileName) as f:
            print(fileName, sum(1 for line in f))
            
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    rTx.replayEvitar(w3,file,thresh,wnd)
    csv_file.close()

    txF.writeTx(w3,'result_algor1.csv',44)


    