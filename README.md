# Consolidated Cashflows sync from SEC 10k filings

This Django application works to allow for a user to quickly sync and review 10k filings from the SEC into a SQL database for analysis


# Running locally

Requirements: Python 3, virtualenv
1) virtualenv env -p python3
2) source env/bin/activate
3) pip install -r requirements.txt
4) python manage.py makemigrations
5) python manage.py migrate
6) python manage.py runserver