import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping


def _make_connection_to_db() -> ptyping.connection:
    return psycopg2.connect(user='postgres',
                            password='1234',
                            host='localhost',
                            port='5432',
                            database='glados_db')


def _close_connection(connection: ptyping.connection, cursor: ptyping.cursor):
    if connection:
        cursor.close()
        connection.close()
        logging.info("Connection to database is closed")


def create_db():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='1234',
                                      host='localhost',
                                      port='5432')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = 'CREATE DATABASE glados_db'
        cursor.execute(sql_create_database)
        logging.info("Create a database glados_db")
    except Error as error:
        logging.error("Error for creating a database", {'error': error})
    finally:
        _close_connection(connection, cursor)


def create_table_users():
    connection = None
    cursor = None
    try:
        connection = _make_connection_to_db()
        cursor = connection.cursor()
        create_table_query = "CREATE TABLE users(" \
                             "id INT PRIMARY KEY NOT NULL, " \
                             "phone VARCHAR(11), " \
                             "name VARCHAR(255) NOT NULL, " \
                             "surname VARCHAR(255) NOT NULL, " \
                             "patroname VARCHAR(255) ," \
                             "university_id VARCHAR(8));"
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("create a table users in database")
    except (Exception, Error) as error:
        logging.error("Error for creating a table users in database", {'error': error})
    finally:
        _close_connection(connection, cursor)
