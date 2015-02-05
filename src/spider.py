#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from grab.spider import Spider, Task
import logging
#import sqlite3
from grab import Grab
from grab.tools import rex
import re
g = Grab()



class ExampleSpider(Spider):
    stations = ('dolgoprud',) #, 'zelen_15'
    #http://www.mosecom.ru/air/air-today/station/zelen_15/table.html
    def task_generator(self):
        for station in self.stations:
            url = 'http://www.mosecom.ru/air/air-today/station/%s/table.html' % station
            yield Task('search', url=url)

    def task_search(self, grab, task):
        thcount=0 #подсчет позиции th в таблице
        tdpdk=0 #подсчет позиции td в таблице
        list1={}
        pok=''
        for elem in grab.doc.select('//th'):
            try:
                #print elem.attr('colspan'), elem.text()
                tdpdk+=2 #когда colspan в th равен 2 то - столбец с пдк второй
                #list[tdpdk] = elem.text().decode('utf-8')
            except:
                tdpdk+=1 #когда отсутствует colspan в th - столбец с пдк первый
#      if ('CO' or 'H2S' or 'PM10' or 'NO') in elem.text() :
#          list1[tdpdk] = elem.text()
            finally:
                #thcount+=1
                pok = re.search("(NO |CO |H2S|PM10)", elem.text())
                if pok:
                    list1[pok.group().strip().lower()] = tdpdk
        print 'количество %s' % thcount

        for key, value in list1.items():
            print key, value
        #print grab.doc.select('//div[@class="s"]//cite').text()


logging.basicConfig(level=logging.DEBUG)
bot = ExampleSpider()
bot.run()