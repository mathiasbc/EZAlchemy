import importlib

from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from constants import SKELETON_URL


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

