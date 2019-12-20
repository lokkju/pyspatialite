# This repository is being archived
Python and Spatialite has come a long way, and this package is no longer as useful as it once was.

Python interface to Spatialite
======

pyspatialite is an interface to the SQLite 3.x embedded relational database engine with spatialite extensions.

It is almost fully compliant with the Python database API version 2.0 and also exposes the unique features of SQLite and spatialite.

Installation
------

```
pip install pyspatialite
```

Pre-release Installation
------
In some cases, the most recent pypi release may be in a pre-release stage.  In order to install pre-release packages, you must include the option '--pre' in your pip command:

```
pip install --pre pyspatialite
```

Usage
-----
pyspatialite extends the sqlite3 interface, and so can be used in place of sqlite3 when modelling spatial information. The main interface is contained in the `pyspatialite.dbapi2` package:

```python
import pyspatialite.dbapi2 as db

con = db.connect(':memory:')

# Test that the spatialite extension has been loaded:
cursor = con.execute('SELECT sqlite_version(), spatialite_version()')
print cursor.fetchall()
# Output should be something like: [(u'3.7.9', u'3.0.1')]
```

For more information on simple pyspatialite usage, see http://www.gaia-gis.it/spatialite-2.4.0-4/splite-python.html

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/lokkju/pyspatialite/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

