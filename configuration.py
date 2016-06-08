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
class ConfigurationService:
 def sftp_connection(self):
  return pysftp.Connection(shost, port=sport, username=slogin, password=spassword) 
 def fdb_connection(self):
  return fdb.connect(dsn=database, user=dlogin, password=dpassword, charset=dcharset)

