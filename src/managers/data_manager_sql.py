import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping
import config_manager as conf


class DataBase:
    user: str
    password: str
    host: str
    port: str
    database: str

    @classmethod
    def config(cls) -> None:
        cls.user = conf.database_user_name()
        cls.password = conf.database_user_password()
        cls.host = conf.database_host()
        cls.port = conf.database_port()
        cls.database = conf.database_name()

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
    def _make_query_without_result(cls, query: str):
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


