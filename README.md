* This readme are just notes for now *
* PGBouncer *
Ran into trouble when using PGBouncer on transaction mode with all tenants having the same db/username/host/port and Tenant TransactionMiddleware.
PGBouncer will think its the same things and not create a new connection from the pool and thus not setting schema on connect.


Running example

python manage.py syncdb
python manage.py syncdb --database a.com
python manage.py syncdb --database b.com
python manage.py syncdb --database c.com
python manage.py syncdb --database d.com
python manage.py runserver


Using Multitenant:
    * No need to modify application code, everything can be routed automatically by using routers
    * Allows for manual routing by using ".using()"
    * Uses builtin Django mechanisms to achieve multitenant
    * Does not use or import threading, uses Django signals which takes care of the locking
    * Thread safe?  (Stress tested it once without problems using gunicorn -w 3,8,11,20,30.  Still needs more testing)
    * Can be slow if bombard with request, but I think thats a server resource issue?
    * 1 database connection per tenant from Django to Database
        * Can be helped by using external connection pooling ie pgbouncer(How Django's multidb method is made, a new connection is made for every entry in the DATABASES setting)
    
    Tenant options:
        1. Single db with single schema
            * All tenants share one db/schema
            * Objects are ForeignKey'ed
        2. Single db with multi schemas
            * 1 schema per tenant
            * Limit to database types supporting namespace like functionality
        3. Multiple db with single schemas
            * 1 db per tenant
            * Mix and match database types
        4. Multiple db with multi schema
            * 1 schema per tenant
            * schemas are sharded across dbs
            * Possibility to mix and match database types


Options:
    MultiDatabase, MultiSchema, SingleDatabase
    
    1 Database with 1 schema, shared with all tenants
    1 DB with multischema, 1 Schema per tenant
    Multiple Database with 1 schema each, 1 database per tenant
    Multiple Database with multischema, sharded schemas, 1 schema per tenant


Pros:
    Multidb:
        Mix and match database types
        True isolation

    Multischema
        
Cons:
    Multidb:
        High cost
