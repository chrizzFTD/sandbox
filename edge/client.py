>>> conn = edgedb.connect('edgedb://edgedb@localhost/edgedb')
>>> r = conn.query("SELECT 1")
>>> r
Set{1}
>>> conn.execute("""
... CREATE TYPE User {
...   CREATE REQUIRED PROPERTY name -> str;
...   CREATE PROPERTY dob -> cal::local_date;
... }
... """)
>>> conn.close()
>>> conn = edgedb.connect('edgedb://edgedb@localhost/edgedb')
>>> user_set = conn.query('SELECT User {name, dob} FILTER .name = <str>$name', name='Christian')
>>> user_set
Set{Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}}
>>>


>>> import datetime
>>> dob = datetime.date(1991, 8, 23)
>>> conn.query("""
... INSERT User {
...   name := <str>$name,
...   dob := <cal::local_date>$dob
... }
... """, name="Christian", dob=dob)
Set{Object{}}
>>> conn.query('SELECT User {name, dob}')
Set{Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}}
>>> r = _
>>> r
Set{Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}}
>>> dir(r)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> r['name']
>>> for i in r:
...     print(i)
...
Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}
>>> r[0]
Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}
>>> dir(r[0])
['__tid__', 'dob', 'id', 'name']
>>> r[0].dob
datetime.date(1991, 8, 23)
>>> type(_)
<class 'datetime.date'>
>>> edgedb.__version__
'0.10.0'
>>> r
Set{Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}}
>>> u = r[0]
>>> u
Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}
>>> u.name
'Christian'
>>> u.dob
datetime.date(1991, 8, 23)
>>>


>>> conn.query("""
... INSERT User {
...   name := <str>$name,
...   dob := <cal::local_date>$dob
... }
... """, name="Anna", dob=datetime.date(1998, 1, 28))
Set{Object{}}
>>> conn.query("""SELECT User""")
Set{Object{}, Object{}}
>>> conn.query("""SELECT User {name, dob}""")
Set{Object{name := 'Christian', dob := datetime.date(1991, 8, 23)}, Object{name := 'Anna', dob := datetime.date(1998, 1, 28)}}
>>> conn.query("""SELECT User {name}""")
Set{Object{name := 'Christian'}, Object{name := 'Anna'}}
