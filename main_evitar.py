import math,csv,time,_thread,os,random, sys
import src.txFunction as txF
import src.initNode as init
import src.replayTx as rTx
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

# MAIN!!


if __name__ == "__main__":

    w3 = Web3(HTTPProvider('http://localhost:8545'))
    thresh = float(sys.argv[1])
    wnd = float(sys.argv[2])
    directory = "./evitar_tx_by_hash/"

    files = os.listdir("./evitar_tx_by_hash")
    files.sort()
    # print(files)

    for file in files:
        fileName = "./evitar_tx_by_hash/"+file
        rTx.replayEvitar(w3,fileName,thresh,wnd)
        rTx.backup(file)

    # fileList = os.listdir("./evitar_tx_by_hash")
    # fileList.sort()
    file =  "./evitar_tx_by_hash/0xe.csv"
          
    rTx.replayEvitar(w3,file,thresh,wnd)

    txF.writeTx(w3,'./result/result_evitar.csv',28)


    