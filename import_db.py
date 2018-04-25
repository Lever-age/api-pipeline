#!/usr/bin/python
# coding: utf-8
import os
import sys
import csv

from datetime import datetime

import sqlalchemy as sa
from database import db_session
from models import Candidate

current_dir = os.path.dirname(os.path.realpath(__file__))

year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year

file_location = current_dir+'/Explorer.Transactions.'+str(year)+'.YTD.txt'

print(file_location)


