#!/usr/bin/python3
# coding: utf-8
import os
import sys
import csv
import re

from datetime import datetime

#import probablepeople

#from postal.parser import parse_address
#from postal.expand import expand_address

import sqlalchemy as sa
from database import db_session
from models import Committee

#from db_cache import ElectionDBCache

#from api_functions import generate_hmac



"""

TRUNCATE contributor;
TRUNCATE contributor_address;
TRUNCATE political_donation;



TRUNCATE candidacy;
TRUNCATE candidate;
TRUNCATE candidate_committees;
TRUNCATE contributor_type;
TRUNCATE party;
TRUNCATE race;


TRUNCATE committee;
TRUNCATE political_donation_contribution_type;
TRUNCATE political_donation_filing_period;

TRUNCATE political_donation_employer_name;
TRUNCATE political_donation_employer_occupation;

"""

reported_by = 'Pennsylvania'

year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year

#csv_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = '/mnt/hgfs/OSX_124/campaign_finance/PA_state/{}/'.format(year)


file_location = csv_dir+'filer_{}.txt'.format(year)

print(file_location)

# amount_list is used to clean the amount
amount_list = list('1234567890.,-')

line_num = 1

csvfile = open(file_location, 'r')

csvreader = csv.reader(csvfile, quotechar='"')

#election_db_cache = ElectionDBCache()
#election_db_cache.load_cache()

#header_row = next(csvreader)   # Get column names

header_row = ['Filer Identification Number', 'Election Year', 'Election Cycle', 'Amended Report Indicator', 'Termination Indicator', 'Filer Type', 'Filer Name', 'Office', 'District', 'Party', 'Filer Address 1', 'Filer Address 2', 'Filer City', 'Filer State', 'Filer Zip Code', 'County', 'Phone Number', 'Beginning Balance', 'Monetary', 'In-Kind', 'Filer Location 1', 'Filer Location 2']

# Remove weird character at beginning of file (\ufeff)
#if header_row[0].find('"') > -1:
#    header_row[0] = header_row[0][header_row[0].find('"'):].strip('"')

#print(header_row);

#ignore_contribution_types = ['Independent Expenditure', 'Campaign Finance Report (Cover Page)', 'Campaign Finance Statement']
#ignore_contribution_types = ['Campaign Finance Report (Cover Page)', 'Campaign Finance Statement', 'Failed Documents']
ignore_contribution_types = []

db_session.begin()

# Delete donations from this year
#sql_query = "DELETE FROM political_donation WHERE year = '{}'".format(year)
#results = db_session.execute(sql_query)

amount_total = 0

committee_name_field = 'Filer Name'

for row in csvreader:

    row_dict = dict(zip(header_row, row))

    committee_name = row_dict[committee_name_field]
    state_id = row_dict['Filer Identification Number']

    try:

        committee = db_session.query(Committee)\
            .filter(Committee.committee_name == committee_name)\
            .filter(Committee.reported_by == reported_by)\
            .filter(Committee.reported_id == state_id)\
            .one()

    except Exception as e:

        committee = Committee()
        committee.committee_name = committee_name
        committee.reported_by = reported_by
        committee.reported_id = state_id

        db_session.add(committee)        
        db_session.commit()
        db_session.begin()


try:
    db_session.commit()
except Exception as e:
    pass

