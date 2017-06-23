#!/usr/bin/env python
# encoding:utf-8
__author__ = 'SY60216'

import sqlite3,sys,re
import SocketServer
from SocketServer import StreamRequestHandler as SRH
from time import ctime

host = '0.0.0.0'
port = 9716
addr = (host,port)

class Servers(SRH):
	def handle(self):
		print 'got connection from ',self.client_address
		conn = sqlite3.connect("/home/nagios/modError.db")
		cur = conn.cursor()
		#self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))
		while True:
			data = self.request.recv(1024)
			if data=="close" or not data: 
				break
			elif data.find("get")!=-1:
				try:
					n=cur.execute("select * from modError;")
					result = cur.fetchall()
					new_list = ""
					for inv in result:
						d = ""
						for i in range(0,len(inv)):
							d = d + "-" + inv[i]
						d = re.sub(r'^-',"",d,0)
						new_list = new_list + "|" + d
					new_list = re.sub(r'^\|',"",new_list,0)
				except sqlite3.Error,e:
					print "sqlite Error:%s\nSQL:%s" %(e,sql)
				if new_list != "":
					#self.request.send(new_list)
					self.wfile.write('%s\n' %new_list)
					print new_list
				else:
					self.request.send("OK\n")
					print "everything is ok!"
				print "RECV from ", self.client_address[0],"\n"
			elif data.find("history")!=-1:
				try:
					n=cur.execute("select * from countData;")
					result = cur.fetchall()
					count_list = ""
					for invC in result:
						d = ""
						for i in range(0,len(invC)):
							d = d + "-" + "%s"%invC[i]
						d = re.sub(r'^-',"",d,0)
						count_list = count_list + "|" + d
					count_list = re.sub(r'^\|',"",count_list,0)
				except sqlite3.Error,e:
					print "sqlite Error:%s\nSQL:%s" %(e,sql)
				if count_list != "":
					#self.request.send(count_list)
					self.wfile.write('%s\n' %count_list)
					print count_list
				else:
					self.request.send("OK\n")
					print "server is have no count data!"
				print "RECV from ", self.client_address[0],"\n"
			else:
				print "rev:",data
				print "RECV from ", self.client_address[0],"\n"
				self.request.send("error\n")
		print 'close connection ',self.client_address,"\n"

#t = SQLClass()
print 'server is running....'
server = SocketServer.ThreadingTCPServer(addr,Servers)
server.serve_forever()



