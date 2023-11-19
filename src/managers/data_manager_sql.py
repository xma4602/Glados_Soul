import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping
import config_manager as conf
from os import path
from string import Template


class DB:
    user: str
    password: str
    host: str
    port: str
    database: str
    scripts_dir: str

    @classmethod
    def config(cls) -> None:
        cls.user = conf.database_user_name()
        cls.password = conf.database_user_password()
        cls.host = conf.database_host()
        cls.port = conf.database_port()
        cls.database = conf.database_name()
        cls.scripts_dir = path.join('files', 'sql')

    @classmethod
    def _create_db(cls) -> None:
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(user=cls.user,
                                    password=cls.password,
                                    host=cls.host,
                                    port=cls.port)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            sql_create_database = f'CREATE DATABASE {cls.database}'
            cursor.execute(sql_create_database)
            logging.info(f"Create a database {cls.database}")
        except Error as error:
            logging.error("Error for creating a database", {'error': error})
        finally:
            cls._close_connection(conn, cursor)

    @classmethod
    def _make_connection(cls) -> ptyping.connection:
        return psycopg2.connect(user=cls.user,
                                password=cls.password,
                                host=cls.host,
                                port=cls.port,
                                database=cls.database)

    @classmethod
    def _close_connection(cls, conn: ptyping.connection, cursor: ptyping.cursor):
        if conn:
            cursor.close()
            conn.close()
            logging.info("Connection to database is closed")

    @classmethod
    def make_query_without_result(cls, query: str):
        conn = cls._make_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        cls._close_connection(conn, cursor)

    @classmethod
    def make_query_with_one_result(cls, query):
        conn = cls._make_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cls._close_connection(conn, cursor)
        return result

    @classmethod
    def make_query_with_list_result(cls, query: str, count: int = 0) -> list:
        conn = cls._make_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        if count:
            result = cursor.fetchmany(count)
        else:
            result = cursor.fetchall()
        cls._close_connection(conn, cursor)
        return result

    @classmethod
    def get_query(cls, file_: str, map_: dict = {}):
        with open(path.join(cls.scripts_dir, file_)) as file:
            query = Template(file.read())
            return query.substitute(map_)


class Users:
    @classmethod
    def create_table(cls):
        create_table_query = "CREATE TABLE users(" \
                             "id INT PRIMARY KEY NOT NULL, " \
                             "phone VARCHAR(11), " \
                             "name VARCHAR(255) NOT NULL, " \
                             "surname VARCHAR(255) NOT NULL, " \
                             "patroname VARCHAR(255) ," \
                             "university_id VARCHAR(8));"
        try:
            DB.make_query_without_result(create_table_query)
            logging.info("create a table users in database")
        except (Exception, Error) as error:
            logging.error("Error for creating a table users in database", {'error': error})

DB.config()
print(DB.get_query(path.join('users', 'create.sql')))
