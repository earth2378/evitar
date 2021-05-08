import src.txFunction as txF
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import sys

w3 = Web3(HTTPProvider('http://localhost:8545'))

dst = sys.argv[1]
block_start = int(sys.argv[2])
block_end = int(sys.argv[3])

txF.extractTx(w3, dst,block_start,block_end)