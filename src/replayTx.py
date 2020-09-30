import csv
import math
import os
import random
import shutil
import time

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.txFunction as txF


# split each tx to their to_address and find the most called contract 
# which is use as max loop in parallel tx sending
def splitTx(src,addressMapping):
    #map to_addres to [tx count, list of tx]
    txPool = dict()
    cmWarning = dict()
    maxLen = 0
    for row in src:
        #row = hash,from_address, to_address, transaction_index, value, 
        #gas, gas_price, input, block_number, receipt_status, error, gasLimit
        toAddress = addressMapping[row[2]]

        if(toAddress not in cmWarning):
            cmWarning[toAddress] = dict()
        
        method = row[7][0:10]
        if(method not in cmWarning[toAddress]):
            cmWarning[toAddress][method] = [0, 0, False] # [txCount, success, warnFlag]

        if(toAddress not in txPool):
            txPool[toAddress] = [1,[row]] # [totalTx, txData]
        else:
            txPool[toAddress][0] += 1
            txPool[toAddress][1].append(row)
            if(txPool[toAddress][0] > maxLen): 
                maxLen = txPool[toAddress][0]

    return txPool, maxLen, cmWarning

# csv_write performance : 0.83 sec/ 10k row
def writeTx(w3,txId):
    txResult = w3.eth.getTransaction(txId.hex())
    txReceipt = w3.eth.getTransactionReceipt(txId.hex())
    file = './tmp/' + txResult.to + '_' + txResult.input[0:10] + '.csv'
    csv_write = open(file,'a',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow([getattr(txReceipt, 'from'),txResult.to,txResult.gas,txReceipt.gasUsed,txReceipt.status])
    csv_write.close()
    return txResult.to, txResult.input[0:10], txReceipt.status

def getBlockGasLimit(file):
    blockGasLimit = dict()
    csv_read = open(file, "r")
    csv_reader = csv.reader(csv_read, delimiter=",")
    csv_reader.__next__()

    for row in csv_reader:
        blockGasLimit[row[0]] = int(row[1])

    print("Block gas limit loaded.")
    
    return blockGasLimit

def backup(file):
    try:
        shutil.rmtree("../database/backup")
    except:
        pass
    os.mkdir("../database/backup")

    src = "../database/nodeEvitar/geth/chaindata"
    dst = "../database/backup/" + file + "/chaindata"
    shutil.copytree(src, dst) 


def backupBM(file):
    try:
        shutil.rmtree("../database/backup")
    except:
        pass
    os.mkdir("../database/backup")

    src = "../database/nodeBaseline/geth/chaindata"
    dst = "../database/backup/B_" + file + "/chaindata"
    shutil.copytree(src, dst) 

    src = "../database/nodeMaxGas/geth/chaindata"
    dst = "../database/backup/M_" + file + "/chaindata"
    shutil.copytree(src, dst)   

#Function to deploy multiple transaction with normal and max gas
def replayBaseLineAndMaxGas(w3,w3_2,file):
    private_key_0, private_key_1 = txF.getPrivateKey(w3,0), txF.getPrivateKey(w3,1)
    nonce_0, nonce_1 = w3.eth.getTransactionCount(w3.eth.accounts[0]), w3.eth.getTransactionCount(w3.eth.accounts[1])

    gas_price = 1000000
    addressMapping, ownerMapping = txF.mapContractInfo('./result/available_contract.csv')
    start_time = time.time()
    count = 0
    blockGasLimit = getBlockGasLimit("./result/block_gas_limit.csv")

    csv_read = open(file, "r")
    csv_reader = csv.reader(csv_read, delimiter=",")
    csv_reader.__next__()

    #row = hash,from_address, to_address, transaction_index, value, gas, gas_price, input, block_number, receipt_status, error
    for row in csv_reader:
        count += 1
        if(count%10000 == 0):
            print(file, count, time.time()-start_time)
        
        #Check is contract owner
        if(row[1] == ownerMapping[row[2]]):
            pk, nonce = private_key_0, nonce_0
            nonce_0 += 1
        else:
            pk, nonce = private_key_1, nonce_1
            nonce_1 += 1

        gas_price += 1
        toAddress = addressMapping[row[2]]

        #sendWithNormal
        try:
            tx = txF.createTx(w3,toAddress,nonce,int(row[4]),int(row[5]),gas_price,row[7],pk)
            txF.sendTx(w3,tx)
        except:
            nonZero = 0
            for char in row[7][2:]:
                if char != "0":
                    nonZero += 1
            
            tx = txF.createTx(w3_2,toAddress,nonce,int(row[4]),int(row[5])+(62*nonZero),gas_price,row[7],pk)
            txF.sendTx(w3,tx)

        #sendWithMaxGas
        tx = txF.createTx(w3_2,toAddress,nonce,int(row[4]),blockGasLimit[row[8]],gas_price,row[7],pk)
        txF.sendTx(w3_2,tx)

        if(count%2000 == 0):
            txF.minePendingTx(w3,1)
            txF.minePendingTx(w3_2,1)


    csv_reader = 0
    csv_read.close()
    txF.minePendingTx(w3,1)
    txF.minePendingTx(w3_2,1)


def replayEvitar(w3,file,thresh,wnd):
    private_key_0, private_key_1 = txF.getPrivateKey(w3,0), txF.getPrivateKey(w3,1) # private key and nonce for both owner and guest
    nonce_0, nonce_1 = w3.eth.getTransactionCount(w3.eth.accounts[0]), w3.eth.getTransactionCount(w3.eth.accounts[1])
    unMine = []  # list that stored pending txId to use for gathering data for warning
    gas_price = 1000000
    addressMapping, ownerMapping = txF.mapContractInfo('./result/available_contract.csv')
    blockGasLimit = getBlockGasLimit("./result/block_gas_limit.csv")
    start_time = time.time()
    count = 0


    csv_read = open(file, "r")
    csv_reader = csv.reader(csv_read, delimiter=",")
    csv_reader.__next__()
    #split all tx to each address
    txPool, maxLen, cmCounterWarn = splitTx(csv_reader,addressMapping)
    print('Load successfully')
    csv_reader = 0
    csv_read.close()
    
    try:
        os.mkdir('./tmp')
    except FileExistsError:
        print('File exist')

    for i in range(maxLen):
        #list of address that all txs are mined, use for clean up some memory
        delAddr = []
        mineFlag = False
        for address in txPool:
            count += 1

            #By pass mined tx
            # if(count < target):
            #     continue
            if(count%10000 == 0):
                print(file, count,time.time()-start_time)
                
            try:
                #row = hash,from_address, to_address, transaction_index, value, gas, gas_price, input, block_number, receipt_status
                row = txPool[address][1][i]
                method = row[7][0:10]
                
                #check that method in address is warned or not
                isWarn = cmCounterWarn[address][method][2]

                #if CM is bad method, avoid sending tx
                if(not isWarn):
                    #create tx for sending to geth, check owner before sending
                    if(row[1] == ownerMapping[row[2]]):
                        tx = txF.createTx(w3,address,nonce_0,int(row[4]),blockGasLimit[row[8]],gas_price,row[7],private_key_0)
                        nonce_0 += 1
                    else:
                        tx = txF.createTx(w3,address,nonce_1,int(row[4]),blockGasLimit[row[8]],gas_price,row[7],private_key_1)
                        nonce_1 += 1

                    #send tx to geth, add txId to pool, set new gas price
                    txId = txF.sendTx(w3,tx)
                    unMine.append(txId) 
                    gas_price += 1
                    cmCounterWarn[address][method][0] += 1 # count tx sent in each CM
                    
                    #when in tmp pool reach thershold, mine and update tx to csv file, reset unMine and cmCounter
                    if((cmCounterWarn[address][method][0]%wnd == 0) or count%2000 == 0):
                        mineFlag = True

            except IndexError: 
                print('out of bound')
            
            #when reach all tx in address, mark address and its tx to be deleted to prevent out of bound error    
            if(txPool[address][0] == i+1): 
                delAddr.append(address)
        
        #mine tx every 2000 tx or reach thershold
        if(mineFlag):
            # print('Mine at %s, at (%s, %s)' % (count, address, method))
            txF.minePendingTx(w3,4)
            for txId in unMine:
                address, method, status = writeTx(w3,txId)
                if(status):
                    cmCounterWarn[address][method][1] += 1

                if(cmCounterWarn[address][method][0]%wnd == 0):
                    successRate = cmCounterWarn[address][method][1]/cmCounterWarn[address][method][0] #successTx / totalTx 
                    if(successRate < thresh):
                        cmCounterWarn[address][method][2] = True
                    else:
                        cmCounterWarn[address][method][2] = False
                    # print('Update at %s, at (%s, %s)' % (count, address, method))
                
            unMine = []     

        #delete address that reach all tx
        for addr in delAddr: 
            #TODO: save state
            del txPool[addr]
    
    
    # print('Mine at %s, at (%s, %s)' % (count, address, method))
    txF.minePendingTx(w3,4)
    for txId in unMine:
        address, method, status = writeTx(w3,txId)
        if(status):
            cmCounterWarn[address][method][1] += 1
            
        if(cmCounterWarn[address][method][0]%wnd == 0):
                    successRate = cmCounterWarn[address][method][1]/cmCounterWarn[address][method][0] #successTx / totalTx 
                    if(successRate < thresh):
                        cmCounterWarn[address][method][2] = True
                    else:
                        cmCounterWarn[address][method][2] = False
                    # print('Update at %s, at (%s, %s)' % (count, address, method))
                

    # Save node current state before continue to new file
    # backup(file)
