import argparse
import csv
import random
import string
import sys
import re


def parse_file(fn):
    rownum = 0
    try:
        with open(fn) as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            for row in reader:
                rownum += 1
                if rownum > 0:
                    update_occurences(row)
                    return row
    except FileNotFoundError:
        return []
    except csv.Error:
        return []


def create_output(n, o):
    ofn = n + '.csv'
    sys.stdout.write(ofn)
    with open(ofn, 'w+', newline='\n', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for l in reversed(sorted(o, key=o.get)):
            numo = o[l]
            label_final = l[0:99]
            print(l, numo)
            writer.writerow([label_final, numo])
    outfile.close()


def update_occurences(row):
    p = re.compile('Sample_characteristics_ch[0-9]_', re.IGNORECASE)
    q = re.compile('_ch[0-9]')
    for label in row:
        label = p.sub('Smp_chr_n_', label)
        label = q.sub('_n', label)
        if label in occurences:
            occurences[label] += 1
        else:
            occurences[label] = 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Put data in database.',
        epilog='''"Space is big. You just won't believe how vastly,
        hugely, mind-bogglingly big it is."'''
    )
    parser.add_argument('--num-files', dest='numfiles', type=int, default=10, required=False,
                        help='number of files to read')
    parser.add_argument('--out-name', dest='oname', type=str, required=False,
                        help='name of output to generate')
    parser.add_argument('--map-file', dest='mapfile', type=str, required=False,
                        help='name of map to use')
    parser.add_argument('--target', dest='target', type=str, default='/', required=False,
                        help='location of files to parse')
    args = parser.parse_args()
    occurences = {}
    fileprefix = args.target + '/'
    if (args.mapfile):
        with open(args.mapfile) as mf:
            for line in mf:
                number = int(re.match('\d+', line).group(0))
                number = number - 200000000
                filenumber = str(number)
                filename = (fileprefix + 'gse' + str(filenumber) + '.tmp')
                sys.stdout.write('item ' + filenumber + ' name ' + filename + '\n')
                header = parse_file(filename)
                if len(header) < 1:
                    sys.stdout.write('+++no file or did not parse\n')
                else:
                    # print(header)
                    sys.stdout.write('*parsed ' + str(len(header)) + ' columns\n')

    else:
        for i in range(args.numfiles + 1):
            # header = []
            filenumber = i + 10000
            filename = (fileprefix + 'gse' + str(filenumber) + '.tmp')
            sys.stdout.write('item ' + str(i) + ' file ' + filename + '\n')
            header = parse_file(filename)
            if len(header) < 1:
                sys.stdout.write('+++no file or did not parse\n')
            else:
                # print(header)
                sys.stdout.write('*parsed ' + str(len(header)) + ' columns\n')

create_output(args.oname, occurences)
