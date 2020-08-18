import math,csv,time,_thread,os,random, logging
import src.txFunction as txF
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

# 1. Run this function

# Function to deploy contract need w3 client and list of contract input
# contract input is in from of  hash, receipt_contract_address, value, gas, gas_price, input
def deployContract(w3):
    counter = 0
    csv_file = open("./source/contract_creation_input.csv","r")
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    
    csv_write = open("result/contract_hash_mapping.csv",'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    private_key = txF.getPrivateKey(w3,0)
    nonce = w3.eth.getTransactionCount(w3.eth.accounts[0])
    start_time = time.time()
    csv_writer.writerow(["txHash", "oldCreator","oldContractAddress"])
    for row in csv_reader:
        # row: hash,from_address, receipt_contract_address,value,gas,gas_price,input
        tx = txF.createContract(w3,nonce,int(row[3]),10000000,10000000,row[6],private_key)
        txId = txF.sendTx(w3,tx)
        nonce += 1
        csv_writer.writerow([txId.hex(),row[1],row[2]])
        # print(txId.hex())

        counter = counter + 1
        if(counter%1000 == 0):
            txF.minePendingTx(w3,2)
            print(counter, time.time()-start_time)
    txF.minePendingTx(w3,2)
    print(time.time()-start_time)

    csv_write.close()
    csv_file.close()

def getAvailableContract(w3):
    csv_file = open("./result/contract_hash_mapping.csv","r")
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)

    csv_write = open('result/available_contract.csv','w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(["txHash", "oldCreator","oldContractAddress","newContractAddress","status"])
    for i in range(0,w3.eth.blockNumber+1):
        txList = w3.eth.getBlock(i).transactions
        for tx in txList:
            data = next(csv_reader, None)
            txReceipt, txResult = w3.eth.getTransactionReceipt(tx), w3.eth.getTransaction(tx)
            if(txReceipt.status == 0):
                if(txResult.gas == txReceipt.gasUsed): 
                    msg = 'All Gas Consumed'
                else: 
                    msg = 'Revert'
            else: 
                msg = 'Success'
            
            if (tx.hex() != data[0]):
                logging.exception("tx hash mismatch")

            csv_writer.writerow([tx.hex(),data[1],data[2],w3.toChecksumAddress(txReceipt.contractAddress),msg])
    
    csv_write.close()
    csv_file.close()
