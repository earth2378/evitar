import math,csv,time,_thread,os,random
import src.txFunction as txF
import src.initNode as init
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

# MAIN!!

# init.deployContract()

if __name__ == "__main__":
    w3 = Web3(HTTPProvider('http://localhost:8544'))
    init.getAvailableContract(w3)