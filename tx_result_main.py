import csv, time, sys

from web3 import HTTPProvider, IPCProvider, Web3, WebsocketProvider

import src.initNode as init
import src.replayTx as rTx
import src.txFunction as txF

# MAIN!! function to count status (bad method) of each status
if __name__ == "__main__":
    # select sourceFile, destFile 
    source = sys.argv[1]
    dst = sys.argv[2]

    result = dict()
    count = 0
    start_time = time.time()

    # read from file and sort status and gas used
    csv_file = open(source,'r+')
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader.__next__()
    for row in csv_reader:
        count += 1
        if(count%1000000 == 0):
            print(count,time.time()-start_time)

        address, method = row[0], row[1]
        gas, gasUsed, status = int(row[2]), int(row[3]), int(row[4])

        if(address not in result):
            result[address] = dict()
        if(method not in result[address]):
            #list of [success,Revert,allGasConsumed]
            result[address][method] = [0,0,0,0,0,0]

        if(gas == gasUsed and status == 0):
            result[address][method][2] += 1
            result[address][method][5] += gasUsed
        elif(status == 0):
            result[address][method][1] += 1
            result[address][method][4] += gasUsed
        elif(status == 1):
            result[address][method][0] += 1
            result[address][method][3] += gasUsed

    csv_file.close()
    
    # write to file
    csv_write = open(dst,'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['Address','Method','Success','Revert','Consumed all gas','S gasUsed','R gasUsed','C gasUsed'])
    for address in result:
        for method in result[address]:
            s = result[address][method]
            csv_writer.writerow([address,method,s[0],s[1],s[2],s[3],s[4],s[5]])
    csv_write.close()