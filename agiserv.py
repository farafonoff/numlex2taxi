import random
import itertools

import known_operators
import db
import db_maxima_asterisk

def getDevicesForNumber(num):
    groups = known_operators.getGroups(db.describeNumber(num))
    devgroups = [db_maxima_asterisk.getDevices(x.group) for x in groups]
    for devs in devgroups:
        random.shuffle(devs)
    devices = itertools.chain(*devgroups)
    channels = [dev.channel for dev in devices]
    return channels

print(known_operators.getGroups(db.describeNumber('9048488073')))
print(known_operators.getGroups(db.describeNumber('89128588538')))
print(known_operators.getGroups(db.describeNumber('+79090561017')))
print(getDevicesForNumber('89128588538'))
print(getDevicesForNumber('+79090561017'))