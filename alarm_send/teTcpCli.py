#!/usr/bin/env python

from socket import *
from time import ctime

HOST = '99.12.90.100'
PORT = 9716
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpCli = socket(AF_INET,SOCK_STREAM)
tcpCli.connect(ADDR)
#tcpServer.bind(ADDR)
#tcpServer.listen(5)

while True:
        #print "waiting connection..."
        #tcpClient,addr = tcpServer.accept()
        #print "accept connect from:",addr

        #while True:
                #data = tcpClient.recv(BUFSIZE)
                #if not data:
                #        break
                #tcpClient.send('[%s] %s' %(ctime(),data))
                #print data
	data = raw_input('> ')
	if not data:
		break
	tcpCli.send(data)
	data2 = tcpCli.recv(BUFSIZE)
	if not data2:
		break
	print data2
        #tcpClient.close()
tcpCli.close()


