#!/usr/bin/env python3
import os
import sys
import re
import time
import logging
import pymysql
import jenkins

# open used file
# usage_log = open('/usr/local/nagios/usage_log', 'a')
nagios = open('/usr/local/nagios/fifo_nagios', 'r')
para_dict = {'LTE_RLABEL':"CBTS00_FSM4_9999_001878_000000", 'SKIP_BUILD':"False"}
job = 'Nagios_usage_build'
token = 'nagios_trigger'
check_sql =  "select * from nagios_instance_usage where host='{}';"
up_id_sql = "update nagios_instance_usage set idle_time=idle_time+0.5,build_time=0 where host='{}';"
up_bu_sql = "update nagios_instance_usage set build_time=build_time+0.5 where host='{}';"
reset_id_ti = "update nagios_instance_usage set idle_time={} where host='{}';"
reset_bu_ti = "update nagios_instance_usage set build_time={} where host='{}';"
in_bu_ti = "insert into nagios_instance_usage (host, build_time) values ('{}', 0.5)"
in_id_ti = "insert into nagios_instance_usage (host, idle_time) values ('{}', 0.5)"

def setup_logger(filename, debug="False"):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:\t%(module)s@%(lineno)s:\t%(message)s')
    ch = logging.StreamHandler()
    if debug.lower() == "true":
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    fh.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def trigger_cbts_build(host):
    log.info("trigger build job")
    server = jenkins.Jenkins("http://hzlinb130.china.nsn-net.net:8080/",
            username='cbts', password='d5867e85334da4487de8a4cdf1923e7f')
    trigger_result = False
    jenkins_node = ''
    host = re.compile(host)
    nodes = server.get_nodes()
    for node in nodes:
        if host.search(node['name']):
            jenkins_node = node['name']
            node_info = server.get_node_info(node['name'])
            idle_status = node_info['idle']
            offline = node_info['offline']
    if jenkins_node and not offline and idle_status:
        log.info("get node ok")
        job_cfg = server.get_job_config(job)
        job_new_cfg = re.sub(r'<assignedNode>.*</assignedNode>',
                    '<assignedNode>{}</assignedNode>'.format(jenkins_node), job_cfg)
        server.reconfig_job(job, job_new_cfg)
        queue_id = server.build_job(job, parameters=para_dict, token=token)
        try:
            queue_info = server.get_queue_item(queue_id)
            i = 0
            while 'executable' not in queue_info:
                i += 1
                if i > 25:
                    return trigger_result
                time.sleep(3)
                queue_info = server.get_queue_item(queue_id)
            log.info("trigger build done")
            trigger_result = server.get_build_info(job, queue_info['executable']['number'])['building']
        except Exception:
            log.warning("trigger maybe failed....")
            trigger_result = True
    del(server)
    return trigger_result

def update_cbts_mysql(user, host, load):
    # create mysql object
    cbts_db = pymysql.connect("10.182.101.80","ca_hzcbtsscm","cloudbts666","CloudBTS" )
    cbts_db.autocommit(1)
    cbts = cbts_db.cursor()
    if float(load) >= 10:
        log.info("Is build load")
        if cbts.execute(check_sql.format(host)):
            log.info("host exist")
            check_output = cbts.fetchall()
            if float(check_output[0][2]) >= 9:
                cbts.execute(reset_bu_ti.format(1.5, host))
            if cbts.execute(up_bu_sql.format(host)):
                log.debug("update build time finish")
            cbts.execute(check_sql.format(host))
            output = cbts.fetchall()
            if float(output[0][2]) >= 1:
                log.info("reset idle time")
                cbts.execute(reset_id_ti.format(0, host))
        else:
            log.info("host not exist,insert it")
            cbts.execute(in_bu_ti.format(host))
    else:
        log.info("Is idle load")
        if cbts.execute(check_sql.format(host)):
            log.info("host exist")
            check_output = cbts.fetchall()
            if float(check_output[0][1]) >= 9:
                cbts.execute(reset_id_ti.format(5.5, host))
            if cbts.execute(up_id_sql.format(host)):
                log.debug("update idle time finish")
            cbts.execute(check_sql.format(host))
            output = cbts.fetchall()
            if float(output[0][1]) > 5:
                if output[0][3] == 'True' and user == 'root':
                    if trigger_cbts_build(host):
                        log.info("build is on going")
                        cbts.execute(reset_id_ti.format(0, host))
        else:
            log.info("host not exist,insert it\n")
            cbts.execute(in_id_ti.format(host))
    cbts_db.close()

log = setup_logger(filename="nagios_trigger.log")
while True:
    usage_info = nagios.readline()
    if usage_info:
        log.info("***** {} *****".format(usage_info.replace('\n', '')))
        usage = usage_info.replace('\n', '').split(':')
        user = usage[0]
        host = usage[1]
        load = usage[3]
        try:
            update_cbts_mysql(user, host, load)
        except Exception:
            log.error("update mysql error,retry....")
            time.sleep(5)
            update_cbts_mysql(user, host, load)
        log.info("***** {} finish *****".format(host))
        # usage_log.flush()
    else:
        nagios.close()
        nagios = open('/usr/local/nagios/fifo_nagios', 'r')
