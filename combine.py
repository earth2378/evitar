import os
import csv
import glob
import sys
import pandas as pd


def combineCSV():
    path = sys.argv[1]
    dest = sys.argv[2]
    mode = sys.argv[3]
    csv.field_size_limit(100000000)

    currentPath = os.getcwd()
    os.chdir(path)
    filePath = os.getcwd()
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    all_filenames.sort()
    for i in range(len(all_filenames)):
        all_filenames[i] = '{}/{}'.format(filePath, all_filenames[i])
        print(all_filenames[i])

    os.chdir(currentPath)

    if mode == 'a':
        combineCSVFast(all_filenames, dest)
    elif mode == 'b':
        combineCSVLowMem(all_filenames, dest)
    else:
        print("Invalid mode: only a and b available")


def combineCSVFast(all_filenames, dest):
    # get file header
    csv_file = open(all_filenames[0], 'r+')
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.__next__()
    csv_file.close()

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv(dest, index=False,
                        columns=header, encoding='utf-8-sig')


def combineCSVLowMem(all_filenames, dest):
    csv_write = open(dest, 'w+', newline='')
    csv_writer = csv.writer(csv_write, delimiter=',')

    writeHeader = False

    for i in all_filenames:
        csv_file = open(i, 'r+')
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = csv_reader.__next__()

        if not writeHeader:
            csv_writer.writerow(header)
            writeHeader = True

        csv_writer.writerows(csv_reader)
        csv_file.close()
        print(i, 'completed')

    csv_write.close()


combineCSV()
