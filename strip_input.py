import csv, os, sys, glob

path = sys.argv[1]
csv.field_size_limit(100000000)
# "../database/maxgasTxs_tmp"
os.chdir(path)

csv_write = open('txs_maxgas.csv','w+',newline = '')
csv_writer = csv.writer(csv_write, delimiter=',')
csv_writer.writerow(['hash','to_address','gas','method'])

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
for i in all_filenames:
    csv_file = open(i,'r+')
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader.__next__()
    for row in csv_reader:
        csv_writer.writerow([row[0],row[1],row[2],row[3][:10]])
    csv_file.close()


csv_write.close()
