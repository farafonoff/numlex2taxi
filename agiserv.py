import known_operators
import db
from pprint import pprint

print(known_operators.getGroups(db.describeNumber('9048488073')))
print(known_operators.getGroups(db.describeNumber('89128588538')))
print(known_operators.getGroups(db.describeNumber('+79090561017')))
