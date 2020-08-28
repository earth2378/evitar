import csv,os, time
    
def initFile():
    files = ['0x1','0x2','0x3','0x4','0x5','0x6','0x7','0x8','0x9','0x0','0xa','0xb','0xc','0xd','0xe','0xf',]
    for file in files:
        csv_write = open("../evitar_tx_by_hash/"+file+".csv","a")
        csv_writer = csv.writer(csv_write, delimiter=',')
        csv_writer.writerow(['hash', 'from_address', 'to_address', 'transaction_index', 'value', 'gas', 'gas_price', 'input', 'block_number', 'receipt_status'])
        csv_write.close()
        

def classifyTx():
    csv.field_size_limit(100000000)
    files = os.listdir("../evitar_tx")
    files.sort()
    count = 0
    start_time = time.time()
    for file in files:
        csv_file = open("../evitar_tx/"+file,"r")
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader.__next__()
        for row in csv_reader:
            count += 1
            if(count%100000 == 0):
                print(count,time.time()-start_time)
            
            csv_write = open("../evitar_tx_by_hash/"+row[7][0:3]+".csv","a")
            csv_writer = csv.writer(csv_write, delimiter=',')
            csv_writer.writerow(row)
            csv_write.close()

initFile()
classifyTx()

