EZAlchemy
=========

Sets a basic start point that you can use to quickly interact with the tables in your existing database.

Installing:

    $ git clone https://github.com/mathiasbc/EZAlchemy.git

Usage:

```python
from EAlchemy import ezalchemy

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
new_car = ezalchemy.create(brand='Audi', year='2009', color='green')
```


