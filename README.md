# Leverage Data Pipeline API


## Setup

**Install OS level dependencies:**

* Python 3.4
* MySQL
* MySQL client libraries + development headers
  + Ubuntu Xenial: `libmysqlclient-dev` package
  + Debian Stretch: `libmariadbclient-dev` package
  + Fedora 26/CentOS 7: `mariadb-devel` package
  + OpenSUSE Leap 42.3: `libmysqlclient-devel` package
  + OS X Sierra: `mysql` homebrew formula
* You will need to set up [libpostal](https://github.com/openvenues/libpostal)

**Install app requirements**

We recommend using [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html) for working in a virtualized development environment. [Read how to set up virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Once you have virtualenvwrapper set up (make sure to initialize as a Python 3 project),

```bash
mkdir leverage
cd leverage
git clone https://github.com/Lever-age/api.git
cd api
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp leverageapi/app_config.py.example leverageapi/app_config.py
```

In `app_config.py`, put your MySQL user in `DB_USER` and password in `DB_PW`.

  NOTE: Mac users might need this [lxml workaround](http://stackoverflow.com/questions/22313407/clang-error-unknown-argument-mno-fused-madd-python-package-installation-fa).

Afterwards, whenever you want to work on leverage-api, cd into the directory

```bash
source venv/bin/activate
```



# Importing Steps

## Clone

``` bash
git clone git@github.com:Lever-age/api-pipeline.git
cd api-pipeline
```

## Create a database.

For now, load the tables.sql file

## Download Files:

### Download Philadelphia files

```bash
wget ftp://ftp.phila-records.com/Year-to-Date%20Transaction%20Files/2017%20YTD/Explorer.Transactions.2017.YTD.txt
```

Note: For years prior to 2017 you can replace 2017 with the year -- but 2018 has a new file name format! Temporarily:
```bash
wget ftp://ftp.phila-records.com/Year-to-Date%20Transaction%20Files/2018%20YTD/2018%20YTD.txt
mv 2018\ YTD.txt Explorer.Transactions.2018.YTD.txt 
```

#### Import
```bash
import_donations_philly.py
```


### Download PA files

Download files from the state's website: [www.dos.pa.gov](https://www.dos.pa.gov/VotingElections/CandidatesCommittees/CampaignFinance/Resources/Pages/FullCampaignFinanceExport.aspx)


Extract into directories by year. You need to import the committees that filed first.

#### Import
```bash
import_donations_pa_filers.py
import_donations_pa.py
```

## Troubleshooting
This project uses Python 3. If you're running both 2 and 3, you need to make sure pip installs the Python 3 libraries. Linux command:

```
sudo python3 -m pip install -r requirements.txt
```

## Errors / Bugs

If something is not behaving intuitively, it is a bug, and should be reported.
Report it here: https://github.com/Lever-age/api-pipeline/issues

## Note on Patches/Pull Requests

* Fork the project.
* Make your feature addition or bug fix.
* Commit, do not mess with rakefile, version, or history.
* Send a pull request. Bonus points for topic branches.

## Copyright

Inspired by Illinois Sunshine.

Copyright (c) 2018 Code for Philly