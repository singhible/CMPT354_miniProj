# Research Grant Council Database Application

This project implements a database application using SQLite and Python for managing research grant proposals and competitions. It provides functionalities to perform various tasks related to managing grant proposals, reviewers, competitions, and organizations.

## Environment Setup and install faker

We used a virtual environment to setup our application. Simply do `python3.12 -m venv ./env/`
`source ./env/bin/activate` in the terminal before you start.

Then install faker using `pip install Faker`

## Database Setup

To set up the database, run the `create_database.py` script. This will create the SQLite database named `council.db` and set up the necessary tables and constraints. After creation you need to run `python3 insert_data.py` to insert the data into the database.

```bash
python create_database.py
```

## To run the application or view the contents

Use the command below to run the application

```bash
python db_app.py
```
Once the application is running, you will be given following options, where options 1-6 relate to the specified tasks in project Step 7, option 7 is for vieweing the table contents and 0 to exit the application:

1. Find open competitions with at least one large proposal in a specific month
2. Find proposal(s) requesting the largest amount of money in a specific area
3. Find proposal(s) submitted before a specific date that are awarded the largest amount of money
4. Output the average requested/awarded discrepancy for a specific area
5. Assign reviewers to review a specific grant application
6. Find the proposal(s) a user needs to review
7. View Table Contents
0. Exit
