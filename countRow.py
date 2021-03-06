import csv, os, glob, sys

def countRowOfFiles():
    path = sys.argv[1]
    csv.field_size_limit(100000000)
    # "../database/maxgasTxs_tmp/txs_baseline.csv"
    os.chdir(path)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    all_filenames.sort()
    for i in all_filenames:
        csv_file = open(i,'r+')
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader) 
        print(i, row_count)
        csv_file.close()

def countRowOfFile():
    path = sys.argv[1]
    csv.field_size_limit(100000000)
    # i = "../database/baselineTx/txs_baseline.csv"
    csv_file = open(path,'r+')
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_count = sum(1 for row in csv_reader) 
    print(path, row_count)
    csv_file.close()


countRowOfFile()