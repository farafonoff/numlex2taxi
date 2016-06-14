# -*- coding: utf-8 -*-
import pysftp,zipfile,csv,io,fdb
from known_operators import parseoperator
from configuration import ConfigurationService
cfg = ConfigurationService()

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

def getlast(dir=dirs_full[0], dry=False):
 if dry:
  return
 with cfg.sftp_connection() as sftp:
  sftp.chdir('numlex/'+dir)
  d = sftp.listdir()
  lastfile=d[-1]
  name,exten = lastfile.split('.');
  lastindex = int(name.split('_')[-1])
  incdiff = lastindex*12;
  print('last full index is {0} inc will be {1}'.format(lastindex, incdiff))
  print('downloading {0}/{1}'.format(dir, lastfile))
  sftp.get(lastfile)
  return ([lastfile], incdiff)

def read_last_index():
 try:
  with io.open('lastinc','r') as file:
   return file.next().strip()
 except IOError as e:
  print e
  return 0

def write_last_index(idx):
 with io.open('lastinc','w') as file:
  file.write(unicode(idx))
 


def get_inc_from(idx,dry=False):
 idx = int(idx)
 nextidx=idx
 if dry:
  return
 files = []
 with cfg.sftp_connection() as sftp:
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
   
def unzip(zipname,dry=False):
 with zipfile.ZipFile(zipname) as zf:
  csv = zf.namelist()[0]
  print csv
  if not dry:
   zf.extract(csv)
  return csv

def cleantable():
 return u"delete from port_new_tmp;\n";

def rowtostatement(row):
 op=row[1]
 num=row[0]
 opnew = parseoperator(op)
 return u"execute procedure af_port_new_insert('{0}','{1}');\n".format(num, opnew)
# return u"insert into port_new_tmp(pphone,poperator) values ('{0}','{1}');\n".format(num, opnew)

def process(files, sqlexecutor):
 for zipname in files:
  csvname = unzip(zipname)
  print 'parsing '+csvname
  with open(csvname, 'rb') as csvfile:
   reader = unicode_csv_reader(csvfile, quotechar=None, quoting=csv.QUOTE_NONE)
   reader.next() #skip header
   lines = 0
   line = 0
   for row in reader:
    if (len(row)>2 and row[2]):
     lines = int(row[2])
     print("total rows in file: {0}".format(lines))
    line = line+1
    if line%100==0:
     if lines>0:
      print("processing line {0} of {1}".format(line,lines))
     else:
      print("processing line {0}".format(line))
    sqlexecutor(rowtostatement(row))

def lprint(x):
 print x

inc = read_last_index()
if inc!=0:
 print("incremental load from {0}".format(inc))
 files, inc = get_inc_from(inc)
else:
 print("load from full file")
 files, inc = getlast()

con = cfg.fdb_connection()
cur = con.cursor()
process(files, lambda x: cur.execute(x))
cur.execute("execute procedure af_port_new_import")
con.commit()

write_last_index(inc)


