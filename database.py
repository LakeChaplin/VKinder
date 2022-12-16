import psycopg2
from system import host, user, password, db_name, offset

# connect to exist database
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True
offset = offset


# create a new table users
def create_users_table():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    page_id integer PRIMARY KEY NOT NULL,
                    first_name varchar(50) NOT NULL,
                    last_name varchar(50) NOT NULL,
                    page_url varchar(50) UNIQUE NOT NULL);"""
            )
            print("[INFO] Table create successfully")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


# insert data into table users
def insert_data_into_users_table(page_id, first_name, last_name, page_url):
    try:
        with connection.cursor() as cursor:
            cursor.execute(("INSERT INTO users "
                            "(page_id, first_name, last_name, page_url)"
                            "VALUES(%(page_id)s, %(first_name)s, %(last_name)s, %(page_url)s)"),
                           {'page_id': page_id,
                            'first_name': first_name,
                            'last_name': last_name,
                            'page_url': page_url
                            })

            print("[INFO] Data into users-table was successfully inserted")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


# create a new table viewed users
def create_viewed_users_table():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS viewed_users(
                    page_id integer PRIMARY KEY NOT NULL);"""
            )
            print("[INFO]Table create successfully")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


# insert data into table viewed users
def insert_data_into_viewed_users_table(page_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(("INSERT INTO viewed_users "
                            "(page_id)"
                            "VALUES(%(page_id)s)"),
                           {'page_id': page_id})
            print("[INFO] Data into viewed users-table was successfully inserted")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


# choosing an unseen profile from table
def unseen_profile():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT  page_id,
                            first_name,
                            last_name,
                            page_url
                            FROM users
                            WHERE page_id NOT IN (SELECT page_id FROM viewed_users WHERE page_id IS NOT NULL)"""
            )
            return cursor.fetchone()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


# delete a users-table
def drop_tables():
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE users;"""
                """DROP TABLE viewed_users;"""

            )
            print("[INFO] all tables was deleted")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
