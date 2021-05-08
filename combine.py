import os, csv, glob, sys
import pandas as pd

def combineCSV():
    path = sys.argv[1]
    dest = sys.argv[2]
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
    combined_csv.to_csv( "./{}".format(dest), index=False, columns=['hash','to_address','gas','input'], encoding='utf-8-sig')

def combineCSVLowMem():
    path = sys.argv[1]
    dest = sys.argv[2]

    csv.field_size_limit(100000000)
    # "../database/baselineTxs"
    os.chdir(path)

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    csv_write = open(dest,'w+',newline = '')
    csv_writer = csv.writer(csv_write, delimiter=',')
    csv_writer.writerow(['hash','to_address','gas','method'])

    writeHeader = False

    count = 1

    for i in all_filenames:
        csv_file = open(i,'r+')
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = csv_reader.__next__()

        if not writeHeader :
            csv_writer.writerow(header)
            writeHeader = True

        for row in csv_reader:
            # for strip txs input only
            # csv_writer.writerow([row[0],row[6],row[8],row[10][:10]])
            csv_writer.writerow(row)

        csv_reader = 0
        csv_file.close()

        print(i, count, "/", len(all_filenames))
        count += 1

    csv_write.close()

combineCSVLowMem()