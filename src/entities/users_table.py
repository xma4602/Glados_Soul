import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping
from os import path
from string import Template
from managers.data_manager_sql import DB
from services import logger


class Users:
    scripts_dir = 'users'
    scripts = {
        'create': "create.sql"
    }

    @classmethod
    def get_query(cls, file_: str):
        return DB.get_query(path.join(cls.scripts_dir, file_))

    @classmethod
    def create(cls):
        script = cls.scripts['create']
        query = cls.get_query(script)
        try:
            DB.make_query_without_result(query)
        except (Error, Exception) as error:
            logging.error('Error by making a query', {'table': 'users', 'query': script, 'error': error})
