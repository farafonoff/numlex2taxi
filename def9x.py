import httplib2
from lxml import html
from known_operators import operators
from collections import defaultdict
from configuration import ConfigurationService

rsurl = 'http://www.rossvyaz.ru/docs/articles/DEF-9x.html'

def get():
 h = httplib2.Http('.cache')
 (headers, content) = h.request(rsurl, 'GET')
 page = html.fromstring(content)
 rows = page.xpath('body/table')[0].findall('tr')
 data = list()
 irows = iter(rows)
 irows.next()
 byregion = defaultdict(lambda :defaultdict(list))
 for row in irows:
  datarow = [c.text.strip() for c in row.getchildren()]
  byregion[datarow[5]][datarow[4]] = datarow
 return byregion


byregion = get()
for region in byregion:
 print region

