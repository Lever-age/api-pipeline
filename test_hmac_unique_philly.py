#!/usr/bin/python3
# coding: utf-8
import os
import sys
import csv
#import re

from datetime import datetime

from api_functions import generate_hmac



current_dir = os.path.dirname(os.path.realpath(__file__))

year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year

file_location = current_dir+'/Explorer.Transactions.'+str(year)+'.YTD.txt'

print(file_location)

line_num = 1

csvfile = open(file_location, 'r')

csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')

header_row = next(csvreader)   # Get column names

# Remove weird character at beginning of file (\ufeff)
if header_row[0].find('"') > -1:
    header_row[0] = header_row[0][header_row[0].find('"'):].strip('"')

#print(header_row);

city_list = []

#ignore_doc_types = ['Independent Expenditure', 'Campaign Finance Report (Cover Page)', 'Campaign Finance Statement']
ignore_doc_types = ['Campaign Finance Report (Cover Page)', 'Campaign Finance Statement', 'Failed Documents']

amount_total = 0

hmac_dict = {}

for row in csvreader:

    line_num += 1

    #if line_num % 10 == 0:
    #    print('line:', line_num)

    #if line_num == 100:
    #    break

    if len(row) != 23:
        print("ERROR: ", line_num, len(row), row)
        continue

    #for i in range(len(row)):
    #    print(type(row[i]))
    #break

    # Get dictionary of row after stripping away white space
    for i in range(len(row)):
        row[i] = row[i].replace('\ufeff', '').strip()

    row_dict = dict(zip(header_row, row))
    #print(row_dict)
    #break

    if row_dict['DocType'] in ignore_doc_types:
        continue

    # Some lines are empty
    if row_dict['Amount'] == '':
        continue

    # Check if this row already imported
    row_hmac_signature = generate_hmac(header_row, row_dict)

    if row_hmac_signature not in hmac_dict:
        hmac_dict[row_hmac_signature] = [line_num]
    else:
        hmac_dict[row_hmac_signature].append(line_num)

#print(hmac_dict)

for hmac_signature in hmac_dict:
    if len(hmac_dict[hmac_signature]) > 1:
        print('Found Error:', hmac_dict[hmac_signature])
