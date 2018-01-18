import random

import known_operators
import db
import db_maxima_asterisk

def getDevicesForNumber(num):
    groups = known_operators.getGroups(db.describeNumber(num))
    devgroups = map(lambda x: db_maxima_asterisk.getDevices(x.group), groups)
    print(list(devgroups))
    for devs in list(devgroups):
        random.shuffle(devs)
    print(list(devgroups))

print(known_operators.getGroups(db.describeNumber('9048488073')))
print(known_operators.getGroups(db.describeNumber('89128588538')))
print(known_operators.getGroups(db.describeNumber('+79090561017')))
getDevicesForNumber('89128588538')