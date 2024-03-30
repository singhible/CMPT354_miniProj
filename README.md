# Research Grant Council Database Application

This project implements a database application using SQLite and Python for managing research grant proposals and competitions. It provides functionalities to perform various tasks related to managing grant proposals, reviewers, competitions, and organizations.

## Environment Setup and install faker

We used a virtual environment to setup our application. Simply do `python3.12 -m venv ./env/`
`source ./env/bin/activate` in the terminal before you start.

Then install faker using `pip install Faker`

## Database Setup

To set up the database, run the `create_database.py` script. This will create the SQLite database named `research_grant_council.db` and set up the necessary tables and constraints.

```bash
python create_database.py
```

## To run the application or view the contents

Use the command below to run the application

```bash
python db_app.py
```

To view the contents of the database you can do the following: `python3 db_app.py --view <table name>` for example, if you want to view the table Competition in our database, do the following:

```bash
python db_app.py --view Competition
```
