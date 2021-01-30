import csv

csv.field_size_limit(100000000)
csv_file = open('../database/baselineTxs/baseline_txs.csv','r+')
csv_reader = csv.reader(csv_file, delimiter=',')

row_count = sum(1 for row in csv_reader) 
print(row_count)

csv_file.close()
