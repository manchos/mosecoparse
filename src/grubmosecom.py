#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "vlad"
__date__ = "$24.01.2015 18:53:54$"
from grab import Grab
from grab.tools import rex
import re
g = Grab()

#g.doc.select('http://www.pvsm.ru', default=None)


g.go('http://www.mosecom.ru/air/air-today/station/zelen_15/table.html')


#print g.response.unicode_body()
print g.response.charset

thcount=0 #подсчет позиции th в таблице
tdpdk=0 #подсчет позиции td в таблице
list1={}
pok=''

for elem in g.doc.select('//th'):
    try:
      #print elem.attr('colspan'), elem.text()
      tdpdk+=2 #когда colspan в th равен 2 то - столбец с пдк второй
      #list[tdpdk] = elem.text().decode('utf-8')
    except:
      tdpdk+=1 #когда отсутствует colspan в th - столбец с пдк первый
#      if ('CO' or 'H2S' or 'PM10' or 'NO') in elem.text() :
#          list1[tdpdk] = elem.text()
    finally:
      thcount+=1
      pok = re.search("(NO |CO |H2S|PM10)", elem.text())
      if pok:
          list1[pok.group().strip().lower()] = tdpdk
#      if re.search("(NO |CO |H2S|PM10)", elem.text()):
#          list1[tdpdk] = elem.text()
      

print 'количество %s' % thcount

for key, value in list1.items():
  print key, value
  
#print g.xpath_text('//tr')
#print g.doc.select('//tr[.//b[text() = "CO"]]').text()

#print g.doc.select('//tr[.//b[text() = "31.01.2015 06:00"]]').select('./td[4]').html()

#.//span[contains(text(),"текст внутри элемента")]

#print int(g.doc.select('count(//tr/th)'))
    
#print g.doc.select('//th[contains(text(),"CO")]').position()
#print g.doc.select('//tr[contains(//b[text() = "23.01.2015 06:00")]').html()
#print g.doc.select('//tr[contains(//b/text(), "31.01.2015 06:00"])]').html()

#position()

#g.xpath('//td[contains(./h3/text(), "Your User Agent")]').text_content()
#print g.rex_text('<caption>([^>]+)</caption>')
#print g.doc.select('//tr[text() = "23.01.2015 06:00"]').text()
print sys.getdefaultencoding() 
if __name__ == "__main__":
    print "Hello World"

