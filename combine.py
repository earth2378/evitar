import os, csv, glob, sys
import pandas as pd

def combineCSV():
    path = sys.argv[1]
    csv.field_size_limit(100000000)
    # "../database/baselineTxs"
    os.chdir(path)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    for i in all_filenames:
        print(i)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "./baseline_txs.csv", index=False, columns=['hash','to_address','gas','input'], encoding='utf-8-sig')

def combineCSVLowMem():
    path = sys.argv[1]
    csv.field_size_limit(100000000)
    # "../database/baselineTxs"
    os.chdir(path)

    extension = 'csv'
    count = 1
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    csv_write = open('txs_baseline.csv','a',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['hash','to_address','gas','method'])

    for i in all_filenames:
        print(i,count, "/443")
        csv_file = open(i,'r+')
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader.__next__()
        for row in csv_reader:
            csv_writer.writerow([row[0],row[1],row[2],row[3][:10]])
        csv_file.close()
        count += 1
        csv_reader = 0

    csv_write.close()

combineCSVLowMem()