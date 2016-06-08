# -*- coding: utf-8 -*-

operators={}
operators['TELE2'] = [u'Т2 Мобайл',u'РТ-Мобайл', u'Ростелеком']
operators['MTS'] = [u'Мобильные ТелеСистемы']
operators['BEELINE'] = [u'ВымпелКом',u'Вымпел-Ком']
operators['MEGAFON'] = [u'МегаФон']

regions={}
regions[18] = [u'Удмурт']
regions[59] = [u'Перм']

def break_quotes(str):
 f1 = str.find('"')
 f2 = str.rfind('"')
 if f2>f1:
  return str[f1+1:f2]
 else:
  return str

def encode(value, kvdict):
 for key, vlist in kvdict.iteritems():
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

