import sys, configparser, pysftp, fdb
Config = configparser.ConfigParser()

if len(sys.argv)>1:
 cfgpath = sys.argv[1]
else:
 cfgpath = 'numlex.cfg'

cfg = Config.read(cfgpath)

def defget(sec, var, default):
 try:
  return Config.get(sec, var)
 except configparser.NoOptionError:
  return default

slogin = Config.get('sftp', 'login')
spassword = Config.get('sftp', 'password')
shost = 'prod-sftp.numlex.ru'
sport = 3232

database = defget('db','database','adminpanel')
dcharset = 'win1251'
dlogin = Config.get('db', 'login')
dpassword = Config.get('db', 'password')
print('database=', database)

tdatabase = defget('taxi','database','taxi')
tcharset = 'win1251'
tlogin = Config.get('taxi', 'login')
tpassword = Config.get('taxi', 'password')

print('database=', tdatabase)

class ConfigurationService:
 def sftp_connection(self):
  return pysftp.Connection(shost, port=sport, username=slogin, password=spassword) 
 def fdb_connection(self):
  return fdb.connect(dsn=database, user=dlogin, password=dpassword, charset=dcharset)
 def taxi_connection(self):
  return fdb.connect(dsn=tdatabase, user=tlogin, password=tpassword, charset=tcharset)

