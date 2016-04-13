
import sqlite3
import os
from sqlalchemy.orm.exc import NoResultFound

from ezalchemy import EZAlchemy


DB_NAME = 'example.db'
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Create table
c.execute(
	"CREATE TABLE Cars (id integer primary key, brand text, color text, year integer)"
)

DB = None

def test_connect():
	global DB 
	DB = EZAlchemy('', '', '', DB_NAME, 'sqlite+pysqlite')
	DB.connect()
	assert 'Cars' in dir(DB)

def test_insert():
	car = DB.insert(DB.Cars, brand='Audi', color='green', year=2009)
	assert car.color == 'green'
	assert car.year == 2009

def test_delete_queryset():
	car = DB.session.query(DB.Cars).filter(DB.Cars.year==2009)
	assert DB.delete(car) == True

def test_delete_obj():
	car = DB.insert(DB.Cars, brand='VW', color='red', year=2016)
	assert DB.delete(car) == True
	no_car = car = DB.session.query(DB.Cars).filter(
		DB.Cars.year==2009,
		DB.Cars.color=='red',
		DB.Cars.brand=='Audi'
	).first()
	assert no_car == None

def test_remove_db():
	conn.close()
	assert os.path.isfile(DB_NAME)
	assert os.remove('example.db') == None


