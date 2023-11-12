import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping
from modules import logger

logger.start()


def _make_connection_to_db() -> ptyping.connection:
    return psycopg2.connect(user='postgres',
                            password='1234',
                            host='localhost',
                            port='5432',
                            database='glados_db')


def _close_connection(conn: ptyping.connection, cursor: ptyping.cursor):
    if conn:
        cursor.close()
        conn.close()
        logging.info("Connection to database is closed")


def create_db():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(user='postgres',
                                password='1234',
                                host='localhost',
                                port='5432')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        sql_create_database = 'CREATE DATABASE glados_db'
        cursor.execute(sql_create_database)
        logging.info("Create a database glados_db")
    except Error as error:
        logging.error("Error for creating a database", {'error': error})
    finally:
        _close_connection(conn, cursor)


def create_table_users():
    conn = None
    cursor = None
    try:
        conn = _make_connection_to_db()
        cursor = conn.cursor()
        create_table_query = "CREATE TABLE users(" \
                             "id INT PRIMARY KEY NOT NULL, " \
                             "phone VARCHAR(11), " \
                             "name VARCHAR(255) NOT NULL, " \
                             "surname VARCHAR(255) NOT NULL, " \
                             "patroname VARCHAR(255) ," \
                             "university_id VARCHAR(8));"
        cursor.execute(create_table_query)
        conn.commit()
        logging.info("create a table users in database")
    except (Exception, Error) as error:
        logging.error("Error for creating a table users in database", {'error': error})
    finally:
        _close_connection(conn, cursor)


def create_table_nicknames():
    conn = None
    cursor = None
    try:
        conn = _make_connection_to_db()
        cursor = conn.cursor()
        create_table_query = "CREATE TABLE nicknames(" \
                             "owner_id INT NOT NULL REFERENCES users(id), " \
                             "named_id INT NOT NULL REFERENCES users(id), " \
                             "nickname VARCHAR(255));"
        cursor.execute(create_table_query)
        conn.commit()
        logging.info('Create a table nicknames in database')
    except (Exception, Error) as error:
        logging.error('Error by creating a table nicknames in database', {"error": error})
    finally:
        _close_connection(conn, cursor)


create_table_users()
create_table_nicknames()
