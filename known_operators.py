# -*- coding: utf-8 -*-

operators={}
operators['TELE2'] = [u'Т2 Мобайл',u'РТ-Мобайл', u'Ростелеком']
operators['MTS'] = [u'Мобильные ТелеСистемы']
operators['BEELINE'] = [u'ВымпелКом',u'Вымпел-Ком']
operators['MEGAFON'] = [u'МегаФон']
operators['YOTA'] = [u'Скартел']

regions={}
regions[18] = [u'Удмурт']
regions[59] = [u'Перм']

class Group:
  def __init__(self, operator, region_id, group, priority = 0):
    self.operator = operator
    self.region_id = region_id
    self.group = group
    self.priority = priority
    
  def match(self, regcode, opercode):
    reg_match = (self.region_id == None) or (self.region_id == regcode)
    opr_match = (self.operator == None) or (self.operator == opercode)
    return (opr_match and reg_match)

  def __str__(self):
    return 'Group<{}>'.format(self.group)
  
  def __repr__(self):
    return 'Group({}, {}, {}, {})'.format(self.operator, self.region_id, self.group, self.priority)

groups=[
  Group('MTS', 18, 'mts_udm', 1000),
  Group('BEELINE', 18, 'beel_udm', 1000),
  Group('MEGAFON', None, 'megafon', 1000),
  Group('TELE2', None, 'tele2', 1000),
  Group('MTS', None, 'mts', 500),
  Group('BEELINE', None, 'beeline', 500),
  Group('YOTA', None, 'yota', 500),
  Group(None, None, 'backup'),
]

def break_quotes(str):
 f1 = str.find('"')
 f2 = str.rfind('"')
 if f2>f1:
  return str[f1+1:f2]
 else:
  return str

def encode(value, kvdict):
 for key, vlist in kvdict.items():
  filtered = [v for v in vlist if (v in value or value in v)]
  if len(filtered)>0:
   return key
 return None

def parseoperator(oldop):
 oldop = break_quotes(oldop)
 encoded = encode(oldop, operators)
 if encoded:
  return encoded
 return oldop

def encoderegion(region):
 return encode(region, regions)

def getGroups(numberinfo):
  nregion = numberinfo.region
  nwho = numberinfo.current_operator
  encregion = encoderegion(nregion)
  encoperator = parseoperator(nwho)
  matched_groups = list(filter(lambda g: g.match(encregion, encoperator), groups))
  return matched_groups
  