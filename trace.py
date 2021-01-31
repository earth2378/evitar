import csv,time
from treelib import Node, Tree

def isNone(i):
    if(i != ''):
        return i
    else :
        return "*"

#This function create tree for  transaction
def createTree(trace_list):
    tree = Tree()
    for trace in trace_list:
        # if(trace[0] == '0x5943a3a24b4e8872b17310125d59701fff8902ffb5a045deb00c684c9d206f54'):
        #     print(trace)
        if(trace[1] == None  or trace[1] == ""):
            tree.create_node(isNone(trace[2]),())
        else : 
            try:
                tree.create_node(isNone(trace[2]),tuple(trace[1].split(',')),tuple(trace[1].split(',')[:-1]))
            except:
                print(trace)
        

    return tree
    
#This  process error of each transaction and write to csv file
def processError(csv_writer,traceTree,txTmp):
    leaves=traceTree.all_nodes()
    errors = []
    for leaf in leaves:
        if(leaf.tag != '*'):
            errors.append(leaf.tag)
    if(len(errors) == 0):
        # errors.append('Success')
        return 1
        
    csv_writer.writerow([txTmp,errors[len(errors)-1]])  

def groupTraceByHash(dstFile,csv_reader):
    csv_write = open(dstFile,'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')

    count = 0
    start_time = time.time()
    trace_list = list()
    txTmp = ''

    #This map add trace to it's transaction's list in trace_pool
    for row in csv_reader:
        count += 1
        if(count%100000 == 0):
            print(count, time.time()-start_time)
        
        # row = [transaction_hash, subtraces, trace_address, error]
        # row = list(row.values())
        if(row[0] == txTmp):
            trace_list.append(row)
        else:
            if(txTmp != ''):
                traceTree = createTree(trace_list)
                processError(csv_writer,traceTree,txTmp)
            txTmp = row[0]
            trace_list = [row]
        
    traceTree = createTree(trace_list)
    processError(csv_writer,traceTree,txTmp)

    print("Trace pool finish")
    csv_write.close()


def getTransactionsError(dst):
    # read trace file
    file = './source/traces_trim_evitar_{}.csv'.format(dst)
    csv_read = open(file, "r")
    csv_reader = csv.reader(csv_read, delimiter=",")
    csv_reader.__next__()

    dstFile = './result/error_identify_evitar_{}.csv'.format(dst)

    groupTraceByHash(dstFile,csv_reader)

    csv_read.close()


# SELECT transaction_hash, trace_address, error
# FROM `ethereum-256603.EthereumTransaction.transaction_trace`
# ORDER BY transaction_hash, trace_address

if __name__ == "__main__":
    getTransactionsError(1)