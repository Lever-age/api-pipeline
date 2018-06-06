#!/usr/bin/python
# coding: utf-8
import os
import sys
import csv
import re

from datetime import datetime

import probablepeople

from postal.parser import parse_address
from postal.expand import expand_address

import sqlalchemy as sa
from database import db_session
from models import Contributor, ContributorAddress, PoliticalDonation

from db_cache import ElectionDBCache

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


current_dir = os.path.dirname(os.path.realpath(__file__))

year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year

file_location = current_dir+'/Explorer.Transactions.'+str(year)+'.YTD.txt'

print(file_location)

# amount_list is used to clean the amount
amount_list = list('1234567890.,-')

total_contributed = 0

line_num = 1

csvfile = open(file_location, 'r')

csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')

election_db_cache = ElectionDBCache()
election_db_cache.load_cache()

header_row = next(csvreader)   # Get column names

# Remove weird character at beginning of file (\ufeff)
if header_row[0].find('"') > -1:
    header_row[0] = header_row[0][header_row[0].find('"'):].strip('"')

#print(header_row);

city_list = []

#ignore_doc_types = ['Independent Expenditure', 'Campaign Finance Report (Cover Page)', 'Campaign Finance Statement']
ignore_doc_types = ['Campaign Finance Report (Cover Page)', 'Campaign Finance Statement', 'Failed Documents']

db_session.begin()

amount_total = 0

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

    ###########################################
    # Custom formatting for certain values
    ###########################################

    # Remove weird characters (like '$') in amount
    row_dict['Amount'] = ''.join([c for c in list(row_dict['Amount']) if c in amount_list])

    row_dict['Amount'] = round(float(row_dict['Amount']), 2)

    # Only store first 5 digits of zipcode
    row_dict['EntityZip'] = row_dict['EntityZip'][:5]




    donation_amount = row_dict['Amount']
    amount_total += row_dict['Amount']
    #continue


    #print('donation:', donation_amount)

    donation_date_obj = datetime.strptime(row_dict['Date'], '%m/%d/%Y')
    donation_submission_date_obj = datetime.strptime(row_dict['SubDate'], '%m/%d/%Y')

    #print(donation_date_obj)

    try:
        committee_id = election_db_cache.return_donation_commitee_id_from_name(row_dict['FilerName'])
    except Exception as e:
        print('ERROR on line:', line_num)
        print(row_dict)
    #print('FilerName:', row_dict['FilerName'], committee_id)

    contribution_type_id = election_db_cache.return_contribution_type_id_from_name(row_dict['DocType'])
    #print('DocType:', row_dict['DocType'], contribution_type_id)

    #contributor_type_id = election_db_cache.return_contributor_type_id_from_name(row_dict[''])
    contributor_type_id = 0

    filing_period_id = election_db_cache.return_filing_period_id_from_name(row_dict['Cycle'])
    #print('Cycle:', row_dict['Cycle'], filing_period_id)

    employer_name_id = 0
    if row_dict['EmployerName'] != '':
        employer_name_id = election_db_cache.return_employer_name_id_from_name(row_dict['EmployerName'])
        #print('EmployerName:', row_dict['EmployerName'], employer_name_id)

    employer_occupation_id = 0
    if row_dict['Occupation'] != '':
        employer_occupation_id = election_db_cache.return_employer_occupation_id_from_name(row_dict['Occupation'])
        #print('Occupation:', row_dict['Occupation'], employer_occupation_id)

    office_id = 0

    is_fixed_asset = 1 if row_dict['Amended'] == 'Y' else 0






    # 'Total of Contributions not exceeding $100'
    is_annonymous = 0
    contributor_id = 0
    contributor_address_id = 0

    if row_dict['EntityName'] == 'Total of Contributions not exceeding $100':
        is_annonymous = 1

    else:

        full_name = contributor_name = row_dict['EntityName']

        bad_name = False
        bad_addy = False

        contributor_name = row_dict['EntityName']
        #print('EntityName:', contributor_name)

        try:
            probablepeople_name = probablepeople.tag(contributor_name)
            #print('probablepeople_name:', probablepeople_name)

            name_type = probablepeople_name[1]

            name_dict = dict(probablepeople_name[0])
            #print('name_dict:', name_dict)

        except Exception as e:
            name_type = 'Unknown'
            name_dict = {'CorporationName': contributor_name}

        if type(name_dict) is not dict:

            print('name ERROR:')
            bad_name = True


        mailing_address = row_dict['EntityAddressLine1']#.upper().replace('  ',', ')
        if row_dict['EntityAddressLine2'] != '':
            mailing_address += ', {}'.format(row_dict['EntityAddressLine2'])

        mailing_address += ', {}, {} {}'.format(row_dict['EntityCity'], row_dict['EntityState'], row_dict['EntityZip']).strip(' ,')

        if mailing_address == '':
            print('ERROR: Empty Address on line {}'.format(line_num))
            bad_addy = True
            address_dict = {}

        else:

            try:

                expanded_address = expand_address(mailing_address)

                parsed_address = parse_address(expanded_address[0])

            except Exception as e:

                print('ERROR: bad address "{}" on line {}'.format(mailing_address, line_num))

                parsed_address = parse_address(mailing_address)

            # Create address dictionary
            address_dict = {d[1]: d[0] for d in parsed_address}
            #print('address_dict:', address_dict)
            #break


            if type(address_dict) is not dict:

                print('addy ERROR:')
                bad_addy = True

        house_number = address_dict['house_number'] if 'house_number' in address_dict else ''
        road = address_dict['road'] if 'road' in address_dict else ''

        city = address_dict['city'] if 'city' in address_dict else ''
        state = address_dict['state'] if 'state' in address_dict else ''
        postcode = address_dict['postcode'] if 'postcode' in address_dict else ''

        #ensure_address_fields_list = ['PlaceName', 'StateName', 'ZipCode']

        #for field in ensure_address_fields_list:
        #    if not bad_addy and field not in address_dict:
        #        address_dict[field] = ''


        # Check if PO Box
        if 'po_box' in address_dict:

            # Get number for PO Box, should be integer after the last space
            potential_po_box_number = address_dict['po_box'][address_dict['po_box'].rfind(' ')+1:]
            if potential_po_box_number.isnumeric():
                address_dict['po_box'] = potential_po_box_number
            else:
                address_dict['po_box'] = address_dict['po_box'][-16:]


            # Get address
            try:

                contributor_address = db_session.query(ContributorAddress)\
                    .filter(ContributorAddress.address_type == 'PO Box')\
                    .filter(ContributorAddress.po_box == address_dict['po_box'])\
                    .filter(ContributorAddress.zipcode == postcode)\
                    .one()

            except Exception as e:


                contributor_address = ContributorAddress()
                contributor_address.address_type = 'PO Box'

                contributor_address.po_box = address_dict['po_box']
                contributor_address.city = city
                contributor_address.state = state
                contributor_address.zipcode = postcode

                db_session.add(contributor_address)        
                #db_session.commit()

            contributor_address_id = contributor_address.id

        else: # Should be a normal address

            addr1 = ''

            addr_build_list = ['house_number', 'road', 'unit']

            for field in addr_build_list:
                if field in address_dict:
                    addr1 = addr1+' '+address_dict[field]

            addr1 = addr1.strip()

            #print addr1
            #if line > 8:
            #    break

            # Get address
            try:

                #print('Checking address')

                contributor_address = db_session.query(ContributorAddress)\
                    .filter(ContributorAddress.address_type == 'Street Address')\
                    .filter(ContributorAddress.addr1 == addr1)\
                    .filter(ContributorAddress.zipcode == postcode)

                #print('obj:', ContributorAddress)

                contributor_address = contributor_address.one()

            except Exception as e:

                #print("Error", e)
                #print("Didn't find address:", addr1)


                contributor_address = ContributorAddress()
                contributor_address.address_type = 'Street Address'

                if 'AddressNumber' in address_dict:
                    number = address_dict['AddressNumber']

                contributor_address.addr1 = addr1
                contributor_address.addr2 = row_dict['EntityAddressLine2'] if 'EntityAddressLine2' in row_dict else ''
                contributor_address.number = house_number
                contributor_address.street = road

                contributor_address.city = city
                contributor_address.state = state
                contributor_address.zipcode = postcode

                db_session.add(contributor_address)        
                #db_session.commit()

            contributor_address_id = contributor_address.id


        #is_person = 1 if name_type == 'Person' else 0
        #is_business = 1 if name_type == 'Corporation' else 0

        is_person = 0
        is_business = 0

        name_prefix = ''
        name_first = ''
        name_middle = ''
        name_last = ''
        name_suffix = ''


        # Only split out name for individuals, 
        if not bad_name and name_type in ['Person', 'Household']:

            is_person = 1

            if 'PrefixMarital' in name_dict: 
                name_prefix = name_dict['PrefixMarital']
            elif 'PrefixOther' in name_dict:
                name_prefix = name_dict['PrefixOther']

            if 'GivenName' in name_dict: 
                name_first = name_dict['GivenName']
            elif 'FirstInitial' in name_dict:
                name_first = name_dict['FirstInitial']

            if 'MiddleName' in name_dict: 
                name_middle = name_dict['MiddleName']
            elif 'MiddleInitial' in name_dict:
                name_middle = name_dict['MiddleInitial']

            if 'Surname' in name_dict: 
                name_last = name_dict['Surname']
            elif 'LastInitial' in name_dict:
                name_last = name_dict['LastInitial']

            if 'SuffixGenerational' in name_dict: 
                name_suffix = name_dict['SuffixGenerational']
            elif 'SuffixOther' in name_dict:
                name_suffix = name_dict['SuffixOther']



            # Check if contributor already exists from first,last,suffix,addr1,zipcode
            try:

                contributor = db_session.query(Contributor)\
                    .filter(Contributor.address_id == contributor_address_id)\
                    .filter(Contributor.name_first == name_first)\
                    .filter(Contributor.name_last == name_last)\
                    .filter(Contributor.name_suffix == name_suffix)\
                    .one()

            except Exception as e:


                contributor = Contributor()
                contributor.address_id = contributor_address_id
                contributor.name_prefix = name_prefix
                contributor.name_first = name_first
                contributor.name_middle = name_middle
                contributor.name_last = name_last
                contributor.name_suffix = name_suffix
                contributor.name_business = ''

                contributor.is_person = is_person
                contributor.is_business = is_business

                db_session.add(contributor)        
                db_session.commit()
                db_session.begin()

            contributor_id = contributor.id

        # Don't store individual names
        elif not bad_name and name_type in ['Corporation', 'Unknown']:

            is_business = 1

            if 'CorporationName' in name_dict:
                corporation = name_dict['CorporationName']

                if 'ShortForm' in name_dict:
                    corporation += ' '+name_dict['ShortForm']

                if 'CorporationNameOrganization' in name_dict:
                    corporation += ' '+name_dict['CorporationNameOrganization']

                if 'CorporationCommitteeType' in name_dict:
                    corporation += ' '+name_dict['CorporationCommitteeType']                        


            else:
                corporation = name_dict['ShortForm']

                if 'CorporationNameBranchType' in name_dict:
                    corporation += ' '+name_dict['CorporationNameBranchType']

                if 'CorporationNameBranchIdentifier' in name_dict:
                    corporation += ' '+name_dict['CorporationNameBranchIdentifier']                        


            # Check if contributor already exists from full_name,addr1,zipcode
            try:

                contributor = db_session.query(Contributor)\
                    .filter(Contributor.address_id == contributor_address_id)\
                    .filter(Contributor.name_business == corporation)\
                    .one()

            except Exception as e:

                contributor = Contributor()
                contributor.address_id = contributor_address_id
                contributor.name_business = corporation

                contributor.is_person = is_person
                contributor.is_business = is_business

                db_session.add(contributor)        
                db_session.commit()
                db_session.begin()

            contributor_id = contributor.id


        else:

            contributor_id = 0



    # Store all donations, including multiple annonymous (under $100) and unknown (badly formed people, address)
    #if True:
    if donation_amount:

        try:

            donation = PoliticalDonation()
            donation.is_annonymous = is_annonymous
            donation.contributor_id = contributor_id
            donation.contributor_type_id = contributor_type_id
            donation.contribution_type_id = contribution_type_id
            donation.committee_id = committee_id
            donation.filing_period_id = filing_period_id
            donation.employer_name_id = employer_name_id
            donation.employer_occupation_id = employer_occupation_id

            donation.donation_date = donation_date_obj 
            donation.donation_submission_date = donation_submission_date_obj
            donation.donation_amount = donation_amount
            donation.provided_name = row_dict['EntityName']
            donation.provided_address = row_dict['EntityAddressLine1']
            donation.is_fixed_asset = is_fixed_asset

            db_session.add(donation)        
            #db_session.commit()

        except Exception as e:
            print("Error saving PoliticalDonation:", e)





    # Save every 1000 lines
    if line_num % 1000 == 0:
        print('storing line:', line_num)
        db_session.commit()
        db_session.begin()

try:
    db_session.commit()
except Exception as e:
    pass


print('amount_total:', amount_total)

