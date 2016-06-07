# -*- coding: utf-8 -*-

operators={}
operators['TELE2'] = [u'Т2 Мобайл',u'РТ-Мобайл',]
operators['MTS'] = [u'Мобильные ТелеСистемы']
operators['BEELINE'] = [u'ВымпелКом']
operators['MEGAFON'] = [u'МегаФон']

regions={}
regions[18] = [u'Удмурт']
regions[59] = [u'Пермск']

def break_quotes(str):
 f1 = str.find('"')
 f2 = str.rfind('"')
 if f2>f1:
  return str[f1+1:f2]
 else:
  return str

def parseoperator(oldop):
 oldop = break_quotes(oldop)
 for opk, ops in operators.iteritems():
  filtered = [op for op in ops if op in oldop]
  if len(filtered)>0:
   return opk
 return oldop


