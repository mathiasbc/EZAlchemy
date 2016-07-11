EZAlchemy
=========

Quickly interact with your database by loading tables to the class EZAlchemy
which also comes with some helpfull methods for inserting and deleting rows
a safe way.

Installing:

    $ pip install ezalchemy

Usage:

```python
from ezalchemy import EZAlchemy

DB = EZAlchemy(
    db_user='username',
    db_password='pezzword',
    db_hostname='127.0.0.1',
    db_database='mydatabase',
    d_n_d='mysql'   # stands for dialect+driver
)


# This function loads all tables in the database to the class instance DB
DB.connect()

# Or just load tables that you need to use, suppose your table is named "Cars"
DB.connect(['Cars'])

# insert elements a safe way
car = DB.insert(DB.Cars, brand='Audi', year=2009, color='green')
print(car.color)

# query all Cars
all_cars = DB.session.query(DB.Cars).all()

# query certain columns (use class attributes for columns)
result = DB.session.query(DB.Cars).filter(DB.Cars.color=='green')
print([r.brand for r in result])

# same query as above (using string for table columns)
DB.session.query(DB.Cars).filter(getattr((DB.cars), 'color') =='green')
print([r.brand for r in result]) 

# change some attributes
green_car = DB.session.query(DB.Cars).filter(DB.Cars.color=='green').first()
green_car.color = 'blue'
blue_car = DB.merge(green_car)
assert blue_car == DB.session.query(DB.Cars).filter(DB.Cars.color=='blue').first()

# delete some elements
result = DB.session.query(DB.Cars).filter(DB.Cars.year < 1980)
DB.delete(result)   # will delete all rows of Cars older than 1980

# delete individual element
new_car = DB.insert(DB.Cars, brand='VW', year=2016, color='red')
DB.delete(new_car)

# We can also use the "engine" to do raw SQL queries
rows = DB.engine.execute('SELECT * from Cars')
for row in rows:
    print(row[0], row[1])
```

Development
-----------

Clone the repository, install dependencies and run the tests:

    $ git clone https://github.com/mathiasbc/EZAlchemy.git
    $ pip install -r dev_requirements.txt
    $ py.test

