#!/usr/bin/python3
# coding: utf-8
import os
import sys
import csv

import sqlalchemy as sa
from database import db_session
from models import VotesmartCandidate


file_location = '/home/chris/projects/philly/git/political-id-match/id_matrix.csv'

#print(file_location)

line_num = 0

csvfile = open(file_location, 'r')

csvreader = csv.reader(csvfile, quotechar='"')

header_row = ['votesmart_candidate_id', 'crp_id', 'fec_id', 'nimsp_candidate_id', 'nimsp_entity_id', 'firstname', \
    'nickname', 'middlename', 'lastname', 'suffix', 'office_state_id', 'election_state_id']

db_session.begin()

# Delete donations from this year
sql_query = "TRUNCATE votesmart_candidates"

results = db_session.execute(sql_query)

for row in csvreader:

    line_num += 1

    if len(row) != len(header_row):
        print("ERROR: ", line_num, len(row), row)
        continue

    row_dict = dict(zip(header_row, row))
    
    candidate = VotesmartCandidate(**row_dict)

    db_session.add(candidate)    

    # Save every 10000 lines
    if line_num % 10000 == 0:
        print('storing line:', line_num)
        db_session.commit()
        db_session.begin()

try:
    db_session.commit()
except Exception as e:
    pass


print('done, #lines: :', line_num)

