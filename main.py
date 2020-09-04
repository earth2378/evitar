import math,csv,time,os,random,shutil
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import src.txFunction as txF
import src.initNode as init


w3 = Web3(HTTPProvider('http://localhost:8544'))

init.deployContract(w3)
# init.getAvailableContract(w3)

# init.checkSuccessfulContract()