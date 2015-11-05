EZAlchemy
=========

Quickly interact with the tables in your existing database. Two different ways to do it, by loading tables to the module, or loading tables to a class EZAlchemy

Installing:

    $ git clone https://github.com/mathiasbc/EZAlchemy.git
    $ cd EZAlchemy
    $ pip install .
    or
    $ python setup.py install

Usage:

Load tables to module
```python
from EZAlchemy import ezalchemy

ezalchemy.connect(
    db_user='username',
    db_password='pezzword',
    db_hostname='127.0.0.1',
    db_database='mydatabase',
    d_n_d='mysql'   # stands for dialect+driver
)
```
At this point connect function dynamically included the tables in the database into the module, so lets suppose I have a table named Cars. I can insert a new row just by doing:

```python
new_car = ezalchemy.Cars().create(brand='Audi', year='2009', color='green')

all_cars = ezalchemy.session.query(ezalchemy.Cars).all()
```

Use the class wrapper with some more functionality
```python
from EZAlchemy.ezalchemy import EZAlchemy

DB = EZAlchemy(
    db_user='username',
    db_password='pezzword',
    db_hostname='127.0.0.1',
    db_database='mydatabase',
    d_n_d='mysql'   # stands for dialect+driver
)

# this function loads all tables in the database to the class instance DB
DB.connectAutoload()
DB.session.query(DB.Cars).all()

# or just load tables that you need to use
DB.connect(['Cars'])
DB.session.query(DB.Cars).all()

# query certain columns
result = DB.session.query(DB.Cars).filter(DB.Cars.color=='green')
print([r.brand for r in result) 

# Insert elements a safe way
car = DB.insert(DB.Cars, brand='Audi', year='2009', color='green')
print(car.color)

# delete some elements
result = DB.session.query(DB.Cars).filter(DB.Cars.color=='green')
DB.delete(result)   # will delete all rows of Cars with color green
```
