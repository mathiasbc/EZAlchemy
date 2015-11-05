from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from constants import SKELETON_URL


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
            obj = tablename(**params)
            self.session.add(obj)
            self.session.commit()
            return obj
        except:
            self.session.rollback()
            raise

    def delete(self, queryset):
        '''delets a row from tha table in database'''
        # TODO: have it receive and object or a queryset
        try:
            for row in queryset:
                self.session.delete(row)
            self.session.commit()
            return True
        except Exception as e:
            print("Error: {}".format(e))
            raise


