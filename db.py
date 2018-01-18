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

def stripCodes(num):
    if num.startswith('8'):
        return num[1:]
    if num.startswith('+7'):
        return num[2:]
    return num

def findRange(num):
    ndef = int(num[0:3])
    nrest = int(num[3:])
    result = select(r for r in Range if (r.rdef == ndef and r.rfrom <=nrest and r.rto >= nrest ) ).first()
    return (result.rwho, result.rregion)

def findMigrated(num):
    mig = Migrated.get(rnumber = num)
    return mig.roperator if mig else mig

class NumberDescription:
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return 'NumberDescriptor<region: {} origin:{} current:{}>'.format(self.region, self.original_operator, self.current_operator)

@db_session
def describeNumber(num):
    num = stripCodes(num)
    base = findRange(num)
    migr = findMigrated(num)
    return NumberDescription(region = base[1], original_operator = base[0], current_operator = migr if migr else base[0])
