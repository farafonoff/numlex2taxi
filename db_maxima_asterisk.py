from pony.orm import *

db = Database()
#set_sql_debug(True)

class Route(db.Entity):
    _table_ = "cc", "routes"
    id = PrimaryKey(int)
    name = Required(str)
    devices = Set("Device")
    
class Device(db.Entity):
    _table_ = "cc", "route_devices"
    id = PrimaryKey(int)
    channel = Required(str)
    route = Required(Route, column="id_route")

db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='asterisk')
db.generate_mapping(create_tables=False)

@db_session
def getDevices(route):
    return list(select(r.devices for r in Route if r.name==route))

@db_session
def tryout():
    select(r.devices for r in Route if r.name=='mts_udm').show()
