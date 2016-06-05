import argparse
import csv
import random
import string
import sys
import re
import os


def parse_file(fn):
    rownum = 0
    try:
        with open(fn) as f:
            sys.stdout.write('opening' + '\n')
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            sys.stdout.write('reader' + '\n')
            for row in reader:
                rownum += 1
                if rownum > 0:
                    update_occurences(row)
                    return row
    except IOError:
        sys.stdout.write('ioerror' + '\n')
        return []
    except csv.Error:
        sys.stdout.write('csv error' + '\n')
        return []


def create_output(n, o):
    sys.stdout.write(n)
    with open(n, 'w+') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for l in reversed(sorted(o, key=o.get)):
            numo = o[l]
            label_final = l[0:99]
            print(l, numo)
            writer.writerow([label_final, numo])
    outfile.close()


def update_occurences(row):
    for label in row:
        label = label.lower()
        if label in occurences:
            occurences[label] += 1
        else:
            occurences[label] = 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Put data in csv.',
    )
    parser.add_argument('--num-files', dest='numfiles', type=int, default=10, required=False,
                        help='number of files to read')
    parser.add_argument('--out-name', dest='outname', type=str, required=False,
                        help='name of output to generate')
    parser.add_argument('--target', dest='target', type=str, default='/', required=False,
                        help='location of files to parse')
    args = parser.parse_args()
    occurences = {}
    fileprefix = args.target + '/'
    i = 0
    for filename in os.listdir(fileprefix):
        fullpath = os.path.join(fileprefix, filename)
        i+=1
        # print(filename)
        sys.stdout.write('item ' + str(i) + ' fullpath ' + fullpath + '\n')
        header = parse_file(fullpath)
        if len(header) < 1:
            sys.stdout.write('+++no file or did not parse\n')
        else:
            # print(header)
            sys.stdout.write('*parsed ' + str(len(header)) + ' columns\n')

    fullOutPath = os.path.join(fileprefix, args.outname)

create_output(fullOutPath, occurences)
