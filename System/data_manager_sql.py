import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import logging
import psycopg2._psycopg as ptyping




class DataBase:

    def config(self):
        pass
    def _create_db(self):
        pass

    def _make_onnection(self):
        pass

    def _close_connection(self):
        pass



class Table:

    _user = 'postgres'
    _password = '1234'
    def __init__(self, name_):
        pass

    def make_connection_to_db(self):


class Users:

    _table = Table('users')