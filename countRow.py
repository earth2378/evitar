import csv, os, glob, sys

path = sys.argv[1]
csv.field_size_limit(100000000)
# "../database/maxgasTxs_tmp"
os.chdir(path)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
for i in all_filenames:
    csv_file = open(i,'r+')
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_count = sum(1 for row in csv_reader) 
    print(i, row_count)
    csv_file.close()
