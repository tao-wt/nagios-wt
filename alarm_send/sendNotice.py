#!/usr/bin/env python
# encoding:utf-8
__author__ = 'sainter'

import sys
#from lib.ParamikoClass import *
#from lib.PublicSQLClass import *
import subprocess
import multiprocessing
import sqlite3
from optparse import OptionParser
import re

class SqliteClass(object):

	def __init__(self,dbname):
		self.dbname = dbname
		self.conn = sqlite3.connect(self.dbname)
		self.cur = self.conn.cursor()

	def query(self,sql):
		try:
			n=self.cur.execute(sql)
			return n
		except sqlite3.Error,e:
			print "sqlite Error:%s\nSQL:%s" %(e,sql)

	def queryAll(self,sql):
		self.query(sql)
		result = self.cur.fetchall()
		new_list =[]
		for inv in result:
			d = []
			for i in range(0,len(inv)):
				d.append(inv[i])
			new_list.append(d)
		return new_list

	def commit(self):
		self.conn.commit()

	def close(self):
		self.cur.close()
		self.conn.close()

class SQLClass(object):
	s = SqliteClass('/home/nagios/modError.db')

	def checkInfo(self,ip,mod):
		sql='select * from modError where ip="%s" and mod="%s";'%(ip,mod)
		return self.s.queryAll(sql)
		
	def insInfo(self,ip,mod):
		sql = 'insert into modError (ip,mod) values("%s","%s");'%(ip,mod)
		#print sql
		self.s.queryAll(sql)
		self.s.commit()

	def delInfo(self,ip,mod):
		sql = "delete from modError where ip='%s' and mod='%s';" %(ip,mod)
		#print sql
		self.s.queryAll(sql)
		self.s.commit()

	def checkCInfo(self,ip,mod):
		sql='select * from countData where ip="%s" and mod="%s";'%(ip,mod)
		return self.s.queryAll(sql)
		
	def insCInfo(self,ip,mod):
		sql = 'insert into countData (ip,mod,count) values("%s","%s",1);'%(ip,mod)
		#print sql
		self.s.queryAll(sql)
		self.s.commit()
	
	def addCInfo(self,ip,mod):
		sql = "update countData set count=count+1 where ip='%s' and mod='%s';"%(ip,mod)
		#print sql
		self.s.queryAll(sql)
		self.s.commit()


parser = OptionParser(add_help_option=0)
# parser.add_option("-h", "--help", action="callback", callback=helpFunc)
# parser.add_option("-v", "-V", "--version", action="callback", callback=verFunc)
parser.add_option("-S", "--stat", action="store", type="string", dest="stat",default="")
parser.add_option("-M", "--module", action="store", type="string", dest="mod",default="")
parser.add_option("-i", "--ip", action="store", type="string", dest="ip",default="")
(options, args) = parser.parse_args()
mod=options.mod
ip=options.ip
stat=options.stat
commandoption=args
#print stat,ip,mod

t = SQLClass()

#checkB = stat.find("OK")
if stat.find("RECOVERY")==-1:
	checkA = t.checkInfo(ip,mod)
	if checkA == []:
		#print '---'
		t.insInfo(ip,mod)
	checkC = t.checkCInfo(ip,mod)
	if checkC == []:
		#print '---'
		t.insCInfo(ip,mod)
	else:
		t.addCInfo(ip,mod)
else:
	checkA = t.checkInfo(ip,mod)
	#print '+++',checkA
	if checkA != []:
		t.delInfo(ip,mod)


