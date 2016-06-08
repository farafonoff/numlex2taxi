from __future__ import print_function
import httplib2
from lxml import html
from known_operators import parseoperator, encoderegion
from collections import defaultdict
from configuration import ConfigurationService

rsurl = 'http://www.rossvyaz.ru/docs/articles/DEF-9x.html'

def get():
 h = httplib2.Http('.cache')
 (headers, content) = h.request(rsurl, 'GET')
 page = html.fromstring(content)
 rows = page.xpath('body/table')[0].findall('tr')
 data = list()
 byregion = defaultdict(lambda :defaultdict(list))
 for row in rows[1:]:
  datarow = [c.text.strip() for c in row.getchildren()]
  numrange = (int(datarow[0]+datarow[1]), int(datarow[0]+datarow[2]))
  byregion[datarow[5]][parseoperator(datarow[4])].append(numrange)
 return byregion

def joinranges(ranges):
 sranges = sorted(ranges, key=lambda range: range[1])
 current = sranges[0]
 result = list()
 for range in sranges[1:]:
  if current[1]+1==range[0]:
   current = (current[0], range[1])
  else:
   result.append(current)
   current = range
 result.append(current)
 return result

#jtest = [(30, 49), (1,2), (3,4) ,(50,100), (6,10)]
#print(jtest)
#print(joinranges([(30, 49), (1,2), (3,4) ,(50,100), (6,10)]))

cfg = ConfigurationService()
con = cfg.fdb_connection()
cur = con.cursor()
#cur.execute('delete from tmp_astmask;')

byregion = get()
for region in byregion:
 eregion = encoderegion(region)
 if eregion:
  vregion = byregion[region]
  for operator, ranges in vregion.items():
   ranges = joinranges(ranges)
   print(region, operator, len(ranges))
   for range in ranges:
    cur.execute(u"execute procedure af_importdefcode('{0}', '{1}', '{2}', {3});".format(range[0], range[1], operator, eregion))
   
con.commit()

