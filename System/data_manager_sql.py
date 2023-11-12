import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


def make_connection_to_db() -> psycopg2.connection:
    return psycopg2.connect(user='postgres',
                            password='1234',
                            host='localhost',
                            port='5432',
                            database='glados_db')


def create_db():
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='1234',
                                      host='localhost',
                                      port='5432')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = 'CREATE DATABASE glados_db'
        cursor.execute(sql_create_database)
    except (Exception, Error) as error:
        print('Error for creating db')
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Conn is closed')


def create_table_users():
    try:
        connection = make_connection_to_db()
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
        print('table created')
    except (Exception, Error) as error:
        print('Error: ', error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Connection is closed')

# id: uuid
# phone:string
# name: string
# surname: string
# patroname: string
# group_id: string
