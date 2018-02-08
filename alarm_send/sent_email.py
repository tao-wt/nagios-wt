#!/usr/bin/env python
import smtplib,string,argparse

def argument():
    parse = argparse.ArgumentParser()
    parse.add_argument('--host', '-H', required=False, help='hostname')
    parse.add_argument('--partition', '-P', required=False, help='partition')
    parse.add_argument('--status', '-S', required=False, default=False, help='partition status')
    parse.add_argument('--text', '-T', required=False, default=False, help='LONGSERVICEOUTPUT')
    return parse.parse_args()

args = argument()
HOST="mail.emea.nsn-intra.net"
SUBJECT="nagios-test"
TO="cbts-cb.scm@nokia.com"
#FROM="tao.8.wang@nokia-sbell.com"
FROM="cbts-cb.scm@nokia.com"
text=args.text
BODY=string.join(("FROM: %s" %FROM,\
                   "TO: %s" %TO,\
                   "Subject: %s:The host %s's %s ." %(args.status,args.host,args.partition),\
                   "",\
                   text
                   ),"\r\n")
server=smtplib.SMTP()
#server.connect(HOST,"25")
#server.starttls()
#server.login("tao.8.wang@nokia-sbell.com","*WTxx201000*")
#server.sendmail(FROM,[TO],BODY)
server.quit()
