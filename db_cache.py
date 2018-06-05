# coding: utf-8

import re

from database import db_session

from models import Candidate, Candidacy, Committee, ContributorAddress, ContributorType, Contributor
from models import Party, PoliticalDonation, PoliticalDonationContributionType, PoliticalDonationEmployerName
from models import PoliticalDonationEmployerOccupation, PoliticalDonationFilingPeriod, Race, State

def return_donation_commitee_id_from_name(name):

    try:

        committee = db_session.query(Committee)\
            .filter(Committee.committee_name == name).one()

    except Exception as e:

        committee = Committee()
        committee.committee_name = name

        db_session.add(committee)        
        db_session.commit()
        db_session.begin()

    return committee.id


def return_contribution_type_id_from_name(name):

    try:

        contribution_type = db_session.query(PoliticalDonationContributionType)\
            .filter(PoliticalDonationContributionType.type_name == name).one()

    except Exception as e:

        contribution_type = PoliticalDonationContributionType()
        contribution_type.type_name = name

        db_session.add(contribution_type)        
        db_session.commit()
        db_session.begin()

    return contribution_type.id


def return_contributor_type_id_from_name(name):

    try:

        contributor_type = db_session.query(ContributorType)\
            .filter(ContributorType.type_name == name).one()

    except Exception as e:

        contributor_type = ContributorType()
        contributor_type.type_name = name

        db_session.add(contributor_type)        
        db_session.commit()
        db_session.begin()

    return contributor_type.id


def return_filing_period_id_from_name(name):

    try:

        filing_period = db_session.query(PoliticalDonationFilingPeriod)\
            .filter(PoliticalDonationFilingPeriod.period_name == name).one()

    except Exception as e:

        filing_period = PoliticalDonationFilingPeriod()
        filing_period.period_name = name

        db_session.add(filing_period)        
        db_session.commit()
        db_session.begin()

    return filing_period.id


def return_employer_name_id_from_name(name):

    try:

        employer_name = db_session.query(PoliticalDonationEmployerName)\
            .filter(PoliticalDonationEmployerName.employer_name == name).one()

    except Exception as e:

        employer_name = PoliticalDonationEmployerName()
        employer_name.employer_name = name

        db_session.add(employer_name)        
        db_session.commit()
        db_session.begin()

    return employer_name.id


def return_employer_occupation_id_from_name(name):

    try:

        occupation = db_session.query(PoliticalDonationEmployerOccupation)\
            .filter(PoliticalDonationEmployerOccupation.occupation_name == name).one()

    except Exception as e:

        occupation = PoliticalDonationEmployerOccupation()
        occupation.occupation_name = name

        db_session.add(occupation)        
        db_session.commit()
        db_session.begin()

    return occupation.id


def return_race_id_from_name_and_district(name, district):

    try:

        race = db_session.query(Race)\
            .filter(Race.race_name == name)\
            .filter(Race.race_district == district).one()

    except Exception as e:

        race = Race()
        race.race_name = name
        race.race_district = district

        db_session.add(office)        
        db_session.commit()
        db_session.begin()

    return office.id






class ElectionDBCache:

    census_last_names = {}    
    state_abbrs = {}

    donation_committees = {}
    contribution_types = {}
    contributor_types = {}
    election_offices  = {}
    employer_names  = {}
    employer_occupations  = {}

    def load_cache(self):


        self.state_abbrs = {}
        state_abbrs = db_session.query(State)
        for s in state_abbrs:
            index = s.abbreviation.upper()
            self.state_abbrs[index] = s.id



        self.donation_committees = {}
        committees = db_session.query(Committee)
        for c in committees:
            index = ''.join(re.findall('([a-z0-9])', c.committee_name.lower()))
            self.donation_committees[index] = c.id

        self.contribution_types = {}
        contribution_types = db_session.query(PoliticalDonationContributionType)
        for c in contribution_types:
            index = ''.join(re.findall('([a-z0-9])', c.type_name.lower()))
            self.contribution_types[index] = c.id


        self.contributor_types = {}
        contributor_types = db_session.query(ContributorType)
        for c in contributor_types:
            index = ''.join(re.findall('([a-z0-9])', c.type_name.lower()))
            self.contributor_types[index] = c.id


        self.election_offices = {}
        election_offices = db_session.query(PoliticalDonationFilingPeriod)
        for c in election_offices:
            index = ''.join(re.findall('([a-z0-9])', c.period_name.lower()))
            self.election_offices[index] = c.id


        self.employer_names = {}
        employer_names = db_session.query(PoliticalDonationEmployerName)
        for c in employer_names:
            index = ''.join(re.findall('([a-z0-9])', c.employer_name.lower()))
            self.employer_names[index] = c.id


        self.employer_occupations = {}
        employer_occupations = db_session.query(PoliticalDonationEmployerOccupation)
        for c in employer_occupations:
            index = ''.join(re.findall('([a-z0-9])', c.occupation_name.lower()))
            self.employer_occupations[index] = c.id


        self.races = {}
        races = db_session.query(Race)
        for c in races:
            index = ''.join(re.findall('([a-z0-9])', c.race_name.lower()+c.race_district))
            if index not in self.races:
                self.races[index] = {}
            self.races[index] = c.id


    def return_census_last_name_id_from_name(self, name):
        index = name.upper()
        if index not in self.census_last_names:
            return 0
        return self.census_last_names[index]


    def return_state_id_from_name(self, name):
        index = name.upper()
        if index not in self.state_abbrs:
            return 0
        return self.state_abbrs[index]




    def return_donation_commitee_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.donation_committees:
            self.donation_committees[index] = return_donation_commitee_id_from_name(name)
        return self.donation_committees[index]


    def return_contribution_type_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.contribution_types:
            self.contribution_types[index] = return_contribution_type_id_from_name(name)
        return self.contribution_types[index]


    def return_contributor_type_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.contributor_types:
            self.contributor_types[index] = return_contributor_type_id_from_name(name)
        return self.contributor_types[index]


    def return_filing_period_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.election_offices:
            self.election_offices[index] = return_filing_period_id_from_name(name)
        return self.election_offices[index]


    def return_employer_name_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.employer_names:
            self.employer_names[index] = return_employer_name_id_from_name(name)
        return self.employer_names[index]


    def return_employer_occupation_id_from_name(self, name):
        index = ''.join(re.findall('([a-z0-9])', name.lower()))
        if index not in self.employer_occupations:
            self.employer_occupations[index] = return_employer_occupation_id_from_name(name)
        return self.employer_occupations[index]


    def return_race_id_from_name_and_district(self, name, district):
        index = ''.join(re.findall('([a-z0-9])', name.lower()+district))
        if index not in self.races:
            self.races[index] = return_race_id_from_name_and_district(name, district)
        return self.races[index]

