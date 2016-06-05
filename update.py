# -*- coding: utf-8 -*-
import pysftp,zipfile,csv,io,fdb
import sys, ConfigParser

Config = ConfigParser.ConfigParser()

cfg = Config.read(sys.argv[1])

slogin = Config.get('sftp', 'login')
spassword = Config.get('sftp', 'password')
shost = 'prod-sftp.numlex.ru'
sport = 3232

database = 'adminpanel'
dcharset = 'win1251'
dlogin = Config.get('db', 'login')
dpassword = Config.get('db', 'password')


##CSV HAck start
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(unicode_csv_data,
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]
##CSV hack end

dirs_full=['Port_All_New']
dirs_inc =['Port_Increment_New','Return_Increment_New']
dirs = dirs_full

def getlast(dir=dirs_full, dry=False):
 if dry:
  return
 with pysftp.Connection(shost, port=sport, username=slogin, password=spassword) as sftp:
  sftp.chdir('numlex/'+dir)
  d = sftp.listdir()
  lastfile=d[-1]
  print 'downloading {0}/{1}'.format(dir, lastfile)
  sftp.get(lastfile)
  return ([lastfile], 11135)

def read_last_index():
 try:
  with io.open('lastinc','r') as file:
   return file.next().strip()
 except IOError as e:
  print e
  return 11133

def write_last_index(idx):
 with io.open('lastinc','w') as file:
  file.write(unicode(idx))
 


def get_inc_from(idx,dry=False):
 idx = int(idx)
 nextidx=idx
 if dry:
  return
 files = []
 with pysftp.Connection(shost, port=sport, username=slogin, password=spassword) as sftp:
  prefix=dirs_inc[0]
  sftp.chdir('numlex/'+dirs_inc[0])
  d = sftp.listdir()
  for fn in d:
   parts = fn.split('_')
   datetime = parts[3]
   index = int(parts[4].split('.')[0])
   if index>idx:
     print 'downloading {0}'.format(fn)
     sftp.get(fn)
     files.append(fn)
     otherfile = '/numlex/{0}/{0}_{1}_{2}.zip'.format(dirs_inc[1], datetime, index)
     print 'downloading {0}'.format(otherfile)
     sftp.get(otherfile)
     files.append('{0}_{1}_{2}.zip'.format(dirs_inc[1], datetime, index))
     nextidx=index
 return (files, nextidx)
   
 
#  lastfile=d[-1]
#  print 'downloading {0}/{1}'.format(dir, lastfile)
#  sftp.get(lastfile)
#  return lastfile



def unzip(zipname,dry=False):
 with zipfile.ZipFile(zipname) as zf:
  csv = zf.namelist()[0]
  print csv
  if not dry:
   zf.extract(csv)
  return csv

def cleantable():
 return u"delete from port_new_tmp;\n";

operators={}
operators['TELE2'] = [u'Т2 Мобайл',u'РТ-Мобайл',]
operators['MTS'] = [u'Мобильные ТелеСистемы']
operators['BEELINE'] = [u'ВымпелКом']
operators['MEGAFON'] = [u'МегаФон']

def replaceop(oldop):
 for opk, ops in operators.iteritems():
  filtered = [op for op in ops if op in oldop]
  if len(filtered)>0:
   return opk
 return oldop

def rowtostatement(row):
 op=row[1]
 num=row[0]
 opnew = replaceop(op[op.find('"')+1:op.rfind('"')])
 return u"execute procedure af_port_new_insert('{0}','{1}');\n".format(num, opnew)
# return u"insert into port_new_tmp(pphone,poperator) values ('{0}','{1}');\n".format(num, opnew)

def process(files, sqlexecutor):
 for zipname in files:
  csvname = unzip(zipname)
  print 'parsing '+csvname
  with open(csvname, 'rb') as csvfile:
   reader = unicode_csv_reader(csvfile, quotechar=None, quoting=csv.QUOTE_NONE)
   reader.next() #skip header
   for row in reader:
    sqlexecutor(rowtostatement(row))

def lprint(x):
 print x

inc = read_last_index()
files, inc = get_inc_from(inc)
#files, inc = getlast(inc)

con = fdb.connect(dsn=database, user=dlogin, password=dpassword, charset=dcharset)
cur = con.cursor()
process(files, lambda x: cur.execute(x))
cur.execute("execute procedure af_port_new_import")
con.commit()

write_last_index(inc)


#with io.open('out.sql', 'w',encoding='utf-8') as sqlfile:
# sqlfile.write(cleantable())
# for dir in dirs:
#  process(dir,lambda x: sqlfile.write(x))


# print reader.next()[1]
# print reader.next()
# print reader.next()

