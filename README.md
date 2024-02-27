# DB-Migration
This Python script facilitates the migration of data from a MySQL database to a PostgreSQL database. It extracts data from specified tables in the MySQL database, transforms it into a pandas DataFrame, and then inserts or updates the data into corresponding tables in the PostgreSQL database. The script also logs the migration process and any errors encountered during execution.

## Features
* Extracts data from specified tables in a MySQL database.
* Transforms data into pandas DataFrames.
* Inserts or updates data into corresponding tables in a PostgreSQL database.
* Logs migration process and errors encountered during execution.

## Requirements
To run the script, you need the following:
```
Python 3.x
pandas
mysql-connector-python
psycopg2-binary
configparser
```
## Installation
1. Clone the repository to your local machine: `git clone https://github.com/Shubham268Mishra/DB-Migration.git`
2. Install the required dependencies: `pip install -r requirements.txt`

# Usage
To migrate data from MySQL to PostgreSQL, follow these steps:

1. Navigate to the project directory: `cd DB-Migration`
2. Run the script with the following command-line arguments: `python migration.py <start_date> <end_date>`

Replace <start_date> and <end_date> with the desired date range for data extraction. The script will extract data from MySQL tables within this date range and insert or update it into corresponding PostgreSQL tables.

## Configuration
Before running the script, make sure to configure the config.ini file with your MySQL and PostgreSQL database credentials. Specify the database host, port, username, password, and database name for both MySQL and PostgreSQL.

Sample config.ini:
```
[MYSQL CREDENTIALS]
USERNAME = your_mysql_username
PASSWORD = your_mysql_password
HOST = mysql_host
PORT = mysql_port
DB_NAME = mysql_database_name

[POSTGRESQL CREDENTIALS]
USERNAME = your_postgresql_username
PASSWORD = your_postgresql_password
HOST = postgresql_host
PORT = postgresql_port
DB_NAME = postgresql_database_name
```
