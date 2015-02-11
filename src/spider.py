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
import sqlite3
import datetime
import time

conn = sqlite3.connect('ecomon.sqlite/ecomon.sqlite')
curs = conn.cursor()


def dtime_to_timestamp(dt):
    dt = ''
    datetime.strptime(dt, "%d.%m.%Y %H:%M")
    time.mktime(dt.timetuple())
    return time.mktime(dt)

def timestamp_to_dtime(timestamp):
    dt = ''
    dt = datetime.fromtimestamp(timestamp)
    return dtime.strftime("%d.%m.%Y %H:%M")  


def enquote1(in_str):
    """Quotes input string with single-quote"""
    in_str = in_str.replace("'", r"\'")
    return "'%s'" % in_str

def enquote2(in_str):
    """Quotes input string with double-quote"""
    in_str = in_str.replace('"', r'\"')
    return '"%s"' % in_str

def gen_insert(table, **kwargs):
    """
    Generates DB insert statement
    """
    cols = []
    vals = []
    for col, val in kwargs.items():
        cols.append(enquote2(col))
        vals.append(enquote1(str(val)))
    cols = ", ".join(cols)
    vals = ", ".join(vals)

    return 'INSERT INTO "%s"(%s) VALUES(%s);' % (
            table, cols, vals)


def gen_update(table,params, where):
    """
    Generates DB update statement
    """
    p = ""
    w = ""
    for col, val in params.items():
        p += "%s = '%s'," % (col, val)
#    for col, val in where.items():
#        w += "%s = '%s' whereP" % (col, val)
    return 'UPDATE %s SET %s WHERE %s;' % (
            table, st[:-1], where)
            
            
class Ecomon:
    curs = ''
    stations = {}
    def __init__(self, curs):
        self.curs = curs
    def get_stations(self):
        #fields = ('address', 'url48', 'ao', 'co_pos', 'no_pos', 'h2s_pos', 'pm10_pos')
        #record = dict.fromkeys(fields, '')
        rowdicts = []
        self.curs.execute('select ecop.*, state.short_name as ao from ecop, state where ecop.state_id = state.id')
        colnames = [desc[0] for desc in self.curs.description]
#        for  row in self.curs.fetchall(): #(address, url48, ao)
#            #rowdict[row[0]] = dict(zip(colnames, row)) 
#            rowdicts.append(dict(zip(colnames, row)))
        rowdicts = [dict(zip(colnames, row)) for row in self.curs.fetchall()]    
        return rowdicts
    
  
    def set_tdposition(self, param, url48):
        cols = []
        vals = []
        self.curs.execute('select ecop.*, state.short_name as ao from ecop, state where ecop.state_id = state.id')
        cursor.execute('''UPDATE ecop SET price = ? WHERE id = ?''', (newPrice, book_id))
        gen_update('ecop', 
        
        
        
        
        for col, val in param.items():
            cols.append(enquote2(col))
            vals.append(enquote1(str(val)))
        

DBecomon = Ecomon(curs)

        
      


class ExampleSpider(Spider):
    stations = DBecomon.get_stations() #, 'zelen_15'
    list1 = {}
    #http://www.mosecom.ru/air/air-today/station/zelen_15/table.html
    def task_generator(self):
        for station in self.stations:
            url = 'http://www.mosecom.ru/air/air-today/station/%s/table.html' % station['url48']
            yield Task('search', url=url, station = station)
    
    def get_tdparametr_position(self, grab, task):
        tdpdk = 0 #finding the position td value in the table
        pok = ''
        pok_s = ''
#        arr = dict(co = '', h2s = '', pm10 = '', no = '')
        arr = {}
        for elem in grab.doc.select('//th'):
            try:
                #print elem.attr('colspan'), elem.text()
                #when in th colspan = 2 - column value of the second
                tdpdk+=2 
            except:
                #when there is no colspan in th - column value of the first
                tdpdk+=1
#      if ('CO' or 'H2S' or 'PM10' or 'NO') in elem.text() :
#          list1[tdpdk] = elem.text()
            finally:
                #thcount+=1
                pok = re.search("(NO |CO |H2S|PM10)", elem.text())
                if pok:
                    pok_s = pok.group().strip().lower()
                    print pok_s
                    arr[pok_s] = tdpdk
                    self.list1[task.station] = arr
                
        #print 'количество %s' % thcount
        #return list1  'jobs': ['programmer', 'writer'],
        
    def get_trtime_position(self, grab):
        text = ''
        time = ''
        dt = ''
#        [last()]
#        grab.doc.select('//th'):
        try:
            #print grab.doc.select('//tr[last()]').select('./td[1][.//b]').html()
            text = grab.doc.select('//tr[last()]').select('./td[1]/b').text()
            dt = datetime.strptime(text, "%d.%m.%Y %H:%M")
        except:
            text = grab.doc.select('//tr[last()]').select('./td[1]').text()
        finally:
            time = re.search("(\d{2}:\d{2})", text)
            
            if time:
                print text, time.group().strip().lower()
#        print g.doc.select('//tr[.//b[text() = "31.01.2015 06:00"]]').select('./td[4]').html()

    def chek_last_time(self, curs):
        """
        Сheck the time of the last saved record
        """
        return 
#        select last_insert_rowid()
    
    
    def task_search(self, grab, task, DBecomon):
        self.get_tdparametr_position(grab, task)
        print self.list1.items()
#        for station, param, position in self.list1.items():
#            print station, param, position
        print task.station['ename'];
        
        self.get_trtime_position(grab)
        #print grab.doc.select('//div[@class="s"]//cite').text()


logging.basicConfig(level=logging.DEBUG)
bot = ExampleSpider()
bot.run()