# check_connections_comm_updates.py
# Author: Klaus Bild
# E-Mail: klaus.bild@webgate.biz
#
# History:
# 20151110 kbild Initial release

#!/usr/bin/python
import ibm_db
import sys
import argparse
import datetime

count = 0
count_warning = 0
count_critical = 0
port = "50000"
peopledb = "peopledb"
communitydb = "SNCOMM"
list = "\n"
list_critical = "\n"
list_warning = "\n"
# Get input parameters

parser = argparse.ArgumentParser(description='This script gets the arguments')
parser.add_argument('-H','--host_ip', help='Host IP ',required=True)
parser.add_argument('-u','--user', help='DB2 user ',required=True)
parser.add_argument('-p','--pw', help='Password',required=True)
parser.add_argument('-w','--warning',help='Warning ', required=True)
parser.add_argument('-c','--critical',help='Critical value ', required=True)
args = parser.parse_args()

uid = args.user
pwd = args.pw
# Connect to DB2 database
try:
    conn_people = ibm_db.connect("DATABASE=" + peopledb + ";HOSTNAME=" + args.host_ip + ";PORT=" + port + ";PROTOCOL=TCPIP;UID=" + uid + ";PWD=" + pwd + ";", "", "")
    conn_comm = ibm_db.connect("DATABASE=" + communitydb + ";HOSTNAME=" + args.host_ip + ";PORT=" + port + ";PROTOCOL=TCPIP;UID=" + uid + ";PWD=" + pwd + ";", "", "")
except:
    print "No connection to DBs:", ibm_db.conn_errormsg()
    sys.exit(3)
# Query DB2 database
sql = "select DISTINCT COMMUNITY_UUID, NAME, LASTMOD from sncomm.community;"
stmt = ibm_db.prepare(conn_comm, sql)
try:
    ibm_db.execute(stmt)
    while ibm_db.fetch_row(stmt) != False:
        name = ibm_db.result(stmt, "NAME")
        lastupdate = ibm_db.result(stmt, "LASTMOD")
        if (datetime.datetime.now() - datetime.timedelta(days=int(args.critical)) > lastupdate):
            count_critical = count_critical + 1
            list_critical = list_critical + name + "\n"
        elif (datetime.datetime.now() - datetime.timedelta(days=int(args.warning)) > lastupdate):
            count_warning = count_warning + 1
            list_warning = list_warning + name + "\n"
except:
    print "Transaction couldn't be completed, error getting communities: " , ibm_db.stmt_errormsg()
    sys.exit(3)

# Nagios standard feedback
if (count_critical!=0):
    print("Critical: There are communites which were not updates since " + args.critical + " days" + list_critical.encode('utf-8') + "| Warning Number=" +  str(count_warning) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(2)
elif (count_warning!=0):
    print("Warning: There are communites which were not updates since " + args.warning + " days" + list_warning.encode('utf-8') + "| Warning Number=" +  str(count_warning) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(1)
elif (count!=0):
    print("Communites are OK " + "| Warning Number=" +  str(count_warning) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(0)

else:
    print("UKNOWN number of Communities without an owner!")
    sys.exit(3)
