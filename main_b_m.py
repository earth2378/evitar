import math,csv,time,_thread,os,random
import src.txFunction as txF
import src.replayTx as rTx
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

# MAIN!!


if __name__ == "__main__":
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    w3_2 = Web3(HTTPProvider('http://localhost:8544'))

    files = os.listdir("./evitar_tx_by_hash")
    files.sort()
    # print(files)

    for file in files:
        fileName = "./evitar_tx_by_hash/"+file
        rTx.replayBaseLineAndMaxGas(w3,w3_2,fileName)
        rTx.backupBM(file)

    txF.writeTx(w3,'./result/result_baseline.csv',28)
    txF.writeTx(w3,'./result/result_maxgas.csv',28)