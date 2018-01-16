from pony.orm import *

db = Database()

class Range(db.Entity):
    rdef = Required(int)
    rfrom = Required(int)
    rto = Required(int)
    rwho = Required(str)
    rregion = Required(str)
    composite_index(rdef, rfrom)

class Migrated(db.Entity):
    rnumber = PrimaryKey(str)
    roperator = Required(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
