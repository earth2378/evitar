import os,csv
import glob
import pandas as pd

def combineCSV():
    csv.field_size_limit(100000000)
    os.chdir("../database/baselineTxs")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    for i in all_filenames:
        print(i)
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "./baseline_txs.csv", index=False, columns=['hash','to_address','gas','input'], encoding='utf-8-sig')


combineCSV()