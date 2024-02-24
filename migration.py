import pandas as pd
import mysql.connector
import configparser
from datetime import datetime
from sys import argv as args
import logging


## Method to read config file settings
def read_config():
    """Reads config.ini and returns the object

    Returns:
        object: config object
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


config = read_config()

# Logger
logging.basicConfig(
    filename="migration_script.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

## MySQL Credentials
MYSQL_USERNAME = config["MYSQL CREDENTIALS"]["USERNAME"]
MYSQL_PASSWORD = config["MYSQL CREDENTIALS"]["PASSWORD"]
MYSQL_HOST = config["MYSQL CREDENTIALS"]["HOST"]
MYSQL_PORT = config["MYSQL CREDENTIALS"]["PORT"]
MYSQL_DB_NAME = config["MYSQL CREDENTIALS"]["DB_NAME"]

## POSTGRESQL Credentials
POSTGRESQL_USERNAME = config["POSTGRESQL CREDENTIALS"]["USERNAME"]
POSTGRESQL_PASSWORD = config["POSTGRESQL CREDENTIALS"]["PASSWORD"]
POSTGRESQL_HOST = config["POSTGRESQL CREDENTIALS"]["HOST"]
POSTGRESQL_PORT = config["POSTGRESQL CREDENTIALS"]["PORT"]
POSTGRESQL_DB_NAME = config["POSTGRESQL CREDENTIALS"]["DB_NAME"]

# Function to format date
def get_user_dates(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(
            start_date_str + " 00:00:00", "%Y-%m-%d %H:%M:%S"
        )
        end_date = datetime.strptime(end_date_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        return start_date, end_date

    except Exception as e:
        print("Invalid date format. Please enter the dates in the format YYYY-MM-DD.")
        logging.error(f"An error occurred while formatting the date: {str(e)}")
        return get_user_dates()

# Define queries and corresponding table names
queries = [
    (
        f"""SELECT * FROM table_1""",
        "table_1",
    ),
    (
        f"""SELECT * FROM table_2""",
        "table_2",
    )
]


def main(start_date, end_date):
    try:
        # Get start and end dates
        start_date, end_date = get_user_dates(start_date, end_date)

        # Establish MySQL connection
        mysql_connection = mysql.connector.connect(
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=MYSQL_DB_NAME
        )

        # Data Extraction and Insertion
        for query, table_name in queries:
            cursor = mysql_connection.cursor(dictionary=True)
            cursor.execute(query)
            mysql_data = cursor.fetchall()
            cursor.close()

            # Convert MySQL data to DataFrame
            mysql_df = pd.DataFrame(mysql_data)

            # Establish PostgreSQL connection
            postgresql_connection = mysql.connector.connect(
                user=POSTGRESQL_USERNAME,
                password=POSTGRESQL_PASSWORD,
                host=POSTGRESQL_HOST,
                port=POSTGRESQL_PORT,
                database=POSTGRESQL_DB_NAME
            )

            # Insert or update data into PostgreSQL
            cursor = postgresql_connection.cursor()
            placeholders = ', '.join(['%s'] * len(mysql_df.columns))
            columns = ', '.join(mysql_df.columns)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE ({columns})=VALUES({columns})"
            cursor.executemany(sql, mysql_df.to_records(index=False))
            postgresql_connection.commit()
            cursor.close()

        logging.info(
            "Queries for {} to {} for table {} are executed and results stored in the Postgresql database.".format(
                start_date, end_date, table_name
            )
        )

    except Exception as e:
        logging.error(f"An error occurred in the execution for {table_name}: {str(e)}")
        raise e

    finally:
        # Close connections
        mysql_connection.close()
        postgresql_connection.close()

if __name__ == "__main__":
    start_date = args[1]
    end_date = args[2]
    main(start_date, end_date)
