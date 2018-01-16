# -*- coding: utf-8 -*-
import pysftp,zipfile,csv,io
from known_operators import parseoperator
from configuration import ConfigurationService
from db import *
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
  return ['Port_All_New_201801160000_1518.zip']
 with cfg.sftp_connection() as sftp:
  sftp.chdir('numlex/'+dir)
  d = sftp.listdir()
  lastfile=d[-1]
  print('downloading {0}/{1}'.format(dir, lastfile))
  sftp.get(lastfile)
  return [lastfile]
   
def unzip(zipname,dry=False):
 with zipfile.ZipFile(zipname) as zf:
  csv = zf.namelist()[0]
  print(csv)
  if not dry:
   zf.extract(csv)
  return csv

def process(files):
 for zipname in files:
  csvname = unzip(zipname)
  print('parsing '+csvname)
  with open(csvname, 'r', encoding='utf-8') as csvfile:
   reader = csv.reader(csvfile, quotechar=None, quoting=csv.QUOTE_NONE, dialect=csv.excel)
   next(reader) #skip header
   lines = 0
   line = 0
   for row in reader:
    if (len(row)>2 and row[2]):
     lines = int(row[2])
     print("total rows in file: {0}".format(lines))
    line = line+1
    if line%10000==0:
     if lines>0:
      print("processing line {0} of {1}".format(line,lines))
     else:
      print("processing line {0}".format(line))
    m = Migrated(rnumber = row[0], roperator = row[1])

files = getlast()
@db_session
def do_work():
  delete(p for p in Migrated)
  process(files)
  commit()

do_work()
