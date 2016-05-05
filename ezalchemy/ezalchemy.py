from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .constants import SKELETON_URL


class EZAlchemy(object):
    '''Wrapper to easily start interacting with database using SQLAlchemy'''

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

    def _bind_table(self, tablename):
        '''Binds a table on the database to the class'''
        new_class = type(str(tablename), (self.Base, object),
            dict(
                __table__=Table(tablename, self.metadata, autoload=True)
            )
        )
        # add new Table class to module
        setattr(self, new_class.__name__, new_class)        

    def connect(self, table_list=None):
        '''Automatically reflects every table on the database'''
        # iterate over tables and bind them to current module
        if table_list:
            table_names = table_list
        else:
            table_names = self.metadata.tables.keys() 
        for tablename in table_names:
            # dynamically define new Table classes
            self._bind_table(tablename)

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

    def merge(self, obj):
        '''Merges or saves an object back to the database'''
        try:
            new_obj = self.session.merge(obj)
            self.session.commit()
            return new_obj
        except:
            self.session.rollback()
            raise

    def delete(self, query_or_obj):
        '''deletes a Query or an obj returned from self.insert'''
        try:
            for row in query_or_obj:
                self.session.delete(row)
            self.session.commit()
            return True
        except TypeError:
            self.session.delete(query_or_obj)
            self.session.commit()
            return True
        except Exception as e:
            print("Error: {}".format(e))
            raise
        return False


