import math,csv,time
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider

def createContract(w3,_nonce,_value,_gas,_gas_price,_input,_private_key):
    tx = dict(
        nonce=_nonce,
        gasPrice=_gas_price,
        gas=_gas,
        to= None,
        value=_value,
        data=_input,
    )
    signed_txn = w3.eth.account.signTransaction(tx,_private_key,)
    return signed_txn

def createTx(w3,_to,_nonce,_value,_gas,_gas_price,_input,_private_key):
    tx = dict(
        nonce=_nonce,
        gasPrice=_gas_price,
        gas=_gas,
        to=_to,
        value=int(_value),
        data=_input,
    )
    signed_txn = w3.eth.account.signTransaction(tx,_private_key,)
    return signed_txn

def sendTx(w3,tx):
    txId = w3.eth.sendRawTransaction(tx.rawTransaction)
    return txId

def minePendingTx(w3,core):
    pendingTx = int(w3.geth.txpool.status()['pending'],0)
    if(pendingTx == 0):
        return 'finished'
    else:
        w3.geth.miner.start(core)
        while(pendingTx != 0):
            pendingTx = int(w3.geth.txpool.status()['pending'],0)
    w3.geth.miner.stop()

def getPrivateKey(w3,account):
    if(account == 0):
        file = './keystore/UTC--2020-08-16T16-14-24.625333000Z--77277497694a2642e05dd14004c80b9da6804611'
    elif(account == 1):
        file = './keystore/UTC--2020-08-16T16-14-39.814045000Z--8455e53c071774a2afcad0f0266671e3a557a62d'
    with open(file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, '1')
    return private_key

def checkTxInBlock(w3,block_start):
    success, fail, oog = 0,0,0
    for i in range(block_start,w3.eth.blockNumber+1):
        txList = w3.eth.getBlock(i).transactions
        #print("Transaction count: "+str(len(txList)))
        for tx in txList:
            txReceipt, txResult = w3.eth.getTransactionReceipt(tx), w3.eth.getTransaction(tx)
            if(txReceipt.status == 0):
                if(txResult.gas == txReceipt.gasUsed): oog += 1
                else: fail += 1
            else: success += 1
    print("Success: "+str(success))
    print("Fail: "+str(fail))
    print("Out of gas: "+str(oog))


def writeTx(w3,fileName,block_start,block_end=0):
    result = dict()
    count = 0
    start_time = time.time()

    if(block_end == 0):
        block_end = w3.eth.blockNumber
    
    for i in range(block_start,block_end+1):
        if(count%1000 == 0):
            print(count,time.time()-start_time)
        count += 1
        txList = w3.eth.getBlock(i).transactions
        for tx in txList:


            txResult = w3.eth.getTransaction(tx.hex())
            txReceipt = w3.eth.getTransactionReceipt(tx.hex())
            #print(tx.hex(),txResult.input[0:10],txReceipt.status,txResult.gas,txReceipt.gasUsed)
            address = txResult.to
            method = txResult.input[0:10]
            if(address not in result):
                result[address] = dict()
            if(method not in result[address]):
                #list of [success,Revert,allGasConsumed]
                result[address][method] = [0,0,0,0,0,0]

            if(txResult.gas == txReceipt.gasUsed and txReceipt.status == 0):
                result[address][method][2] += 1
                result[address][method][5] += txReceipt.gasUsed
            elif(txReceipt.status == 0):
                result[address][method][1] += 1
                result[address][method][4] += txReceipt.gasUsed
            elif(txReceipt.status == 1):
                result[address][method][0] += 1
                result[address][method][3] += txReceipt.gasUsed
    
    csv_write = open(fileName,'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['Address','Method','Success','Revert','Consumed all gas','S gasUsed','R gasUsed','C gasUsed'])
    for address in result:
        for method in result[address]:
            s = result[address][method]
            csv_writer.writerow([address,method,s[0],s[1],s[2],s[3],s[4],s[5]])
    csv_write.close()

# function for map oldAddress -> newAddress and oldOwner -> newOwner
def mapContractInfo(file):
    # contract mapping file
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader.__next__()
        contractAddressMapping = dict()
        ownerMapping = dict()
        for row in csv_reader:
            # row: hash, oldCreator, oldContractAddress, newContractAddress, status
            contractAddressMapping[row[2]] = row[3]
            ownerMapping[row[2]] = row[1]

    print("Contract mapping finished.")
    return contractAddressMapping,ownerMapping

def txGasUsed(w3,fileName,block_start,block_end=0):
    count = 0
    start_time = time.time()

    if(block_end == 0):
        block_end = w3.eth.blockNumber

    csv_write = open(fileName,'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['Status','gasUsed'])

    for i in range(block_start,block_end+1):
        if(count%1000 == 0):
            print(count,time.time()-start_time)
        count += 1
        txList = w3.eth.getBlock(i).transactions
        for tx in txList:

            txResult = w3.eth.getTransaction(tx.hex())
            txReceipt = w3.eth.getTransactionReceipt(tx.hex())
        

            if(txResult.gas == txReceipt.gasUsed and txReceipt.status == 0):
                csv_writer.writerow(['consumed-all-gas',txReceipt.gasUsed])
            elif(txReceipt.status == 0):
                csv_writer.writerow(['revert',txReceipt.gasUsed])
            elif(txReceipt.status == 1):
                csv_writer.writerow(['success',txReceipt.gasUsed])
    csv_write.close()

def getEtherUsedAsGasBaseline():
    csv_file1 = open('A.csv','r') # tx_input
    csv_reader1 = csv.reader(csv_file1, delimiter=',')
    csv_file2 = open('B.csv','r') # gasUsed and status
    csv_reader2 = csv.reader(csv_file2, delimiter=',')
    csv_reader1.__next__()
    csv_reader2.__next__()

    file1,file2 = [],[]
    for row in csv_reader1:
        file1.append([row[5],row[6]]) # gas, gasPrice
    for row in csv_reader2:
        file2.append(row) # status, gasUsed
    csv_file1.close()
    csv_file2.close()

    value_revert = 0
    value_cag = 0
    value_success = 0
    for i in range(len(file1)):
        if(file2[i][0] == 'consumed-all-gas'):
            value_cag += (file1[i][1]/1000000) * file2[i][2]
        elif(file2[i][0] == 'revert'):
            value_revert += (file1[i][1]/1000000) * file2[i][2]
        elif(file2[i][0] == 'success'):
            value_success += (file1[i][1]/1000000) * file2[i][2]
    
    value_revert = value_revert/1000000000000
    value_cag = value_cag/1000000000000
    value_success = value_success/1000000000000
    csv_write = open('gasUsedBaseline','w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['Success', 'Revert', 'Consumed All Gas'])
    csv_writer.writerow([value_success, value_revert, value_cag])
    csv_write.close()