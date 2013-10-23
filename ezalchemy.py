#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import importlib

from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__author__ = "Mathias Bustamante"
__email__ = "mathiasbc@gmail.com"

# dialect+driver://username:password@host:port/database
SKELETON_URL = '%(dialect_driver)s://%(user)s:%(pass)s@%(host)s/%(database)s'

# global variable session
session = None


class BaseTable(object):
    '''Base table class for tables to be declared by the user'''

    def create(self, **params):
        '''Wraps the try: commit() except: rollback for easier usage'''
        obj = self.__class__(**params)
        session.add(obj)
        try:
            session.commit()
            return obj
        except:
            session.rollback()
            raise

def connect(db_user, db_password, db_hostname, db_database, d_n_d='mysql'):
    '''Builds the URL to connect to the database and connects'''
    DB_URL = SKELETON_URL % {
        'dialect_driver': d_n_d,
        'user': db_user,
        'pass': db_password,
        'host': db_hostname,
        'database': db_database,
    }

    #Create and engine and get the metadata
    Base = declarative_base()
    engine = create_engine(DB_URL)
    metadata = MetaData(bind=engine)
    metadata.reflect(engine)

    #Create a session to use the tables
    Session = sessionmaker(bind=engine)
    global session
    session = Session()

    # Get the name of the corrunt module
    current_module = importlib.import_module(__name__)

    # iterate over tables and append them to current module
    for tablename in metadata.tables.keys():
        # dynamically define new Table classes
        new_class = type(str(tablename), (Base, BaseTable),
            dict(
                __table__=Table(tablename, metadata, autoload=True)
            )
        )
        # add new Table class to module
        setattr(current_module, new_class.__name__, new_class)


class EZAlchemy(object):
    ''' Wrapper to easily start interacting with database using SQLAlchemy'''

    def __init__(
        self, db_user, db_password, db_hostname, db_database, d_n_d='mysql'
    ):
        '''Builds the URL to connect to the database and connects'''
        DB_URL = SKELETON_URL % {
            'dialect_driver': d_n_d,
            'user': db_user,
            'pass': db_password,
            'host': db_hostname,
            'database': db_database, 
        }
        #Create and engine and get the metadata
        self.Base = declarative_base()
        self.engine = create_engine(DB_URL)
        self.metadata = MetaData(bind=self.engine)
        self.metadata.reflect(self.engine)
        #Create a session to use the tables
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def connectAutoload(self):
        '''Automatically reflects every table on the database'''
        # iterate over tables and append them to current module
        for tablename in self.metadata.tables.keys():
            # dynamically define new Table classes
            new_class = type(str(tablename), (self.Base, object),
                dict(
                    __table__=Table(tablename, self.metadata, autoload=True)
                )
            )
            # add new Table class to module
            setattr(self, new_class.__name__, new_class)

    def connect(self, tables_list):
        '''Reflects only the tables specified in tables list'''
        for tablename in tables_list:
            # dynamically define new Table classes
            new_class = type(str(tablename), (self.Base, object),
                dict(
                    __table__=Table(tablename, self.metadata, autoload=True)
                )
            )
            # add new Table class to module
            setattr(self, new_class.__name__, new_class)

    def insert(self, tablename, **params):
        '''inserts a new row to the table on database'''
        try:
            obj = self.tablename(**params)
            session.add(obj)
            session.commit()
            return obj
        except:
            session.rollback()
            raise

    def delete(self, tablename, obj_instance):
        '''delets a row from tha table in database'''
        raise NotImplemented





