from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from known_operators import parseoperator, encoderegion
from collections import defaultdict
from configuration import ConfigurationService
from db import *

rsurl = 'https://www.rossvyaz.ru/docs/articles/DEF-9x.html'

def fetchUrl():
  return requests.get(rsurl).content

def loadFile():
  with open('DEF-9x.html', 'r', encoding='cp1251') as myfile:
    return myfile.read()

def loadToDb():
 r = loadFile()
 soup = BeautifulSoup(r, 'html.parser')
 rows = soup.find('table').find_all('tr')
 data = list()
 byregion = defaultdict(lambda :defaultdict(list))
 for row in rows[1:]:
  lrow = row.find_all('td')
  datarow = [c.get_text().strip() for c in lrow]
  r = Range(rdef = int(datarow[0]), rfrom = datarow[1], rto = datarow[2], rwho = datarow[4], rregion = datarow[5])
  data.append(r)
 return data

@db_session
def reinit_ranges():
  #set_sql_debug(True)
  delete(p for p in Range)
  data = loadToDb()
  print(len(data), 'rows')
  commit()

reinit_ranges()
