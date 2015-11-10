# check_connections_comm_owners.py
# Author: Klaus Bild
# E-Mail: klaus.bild@webgate.biz
#
# History:
# 20151110 kbild Initial release


#!/usr/bin/python
import ibm_db
import sys
import argparse

count = 0
port = "50000"
peopledb = "peopledb"
communitydb = "SNCOMM"
list = "\n"

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

def check_if_user_active(prof_uid_lower):
    sql = "select PROF_MAIL from EMPINST.employee where prof_uid_lower = '" + prof_uid_lower + "' and prof_state = '0';"
    stmt = ibm_db.prepare(conn_people, sql)
    try:
        ibm_db.execute(stmt)
        if ibm_db.fetch_row(stmt):
            return True
        else:
            return False
    except:
        print "Transaction couldn't be completed, error getting profiles data: " , ibm_db.stmt_errormsg()
        sys.exit(3)

def check_community_owners(community_id):
    active = False
    sql = "select DISTINCT LOWER_LOGIN from sncomm.memberlogin where member_uuid in (SELECT DISTINCT MEMBER_UUID from sncomm.member WHERE COMMUNITY_UUID = '" + community_id + "' AND ROLE='1' AND LOWER_LOGIN NOT LIKE '%@%');"
    stmt = ibm_db.prepare(conn_comm, sql)
    try:
        ibm_db.execute(stmt)
        while ibm_db.fetch_row(stmt) != False:
            member_login = ibm_db.result(stmt, 0)
            if check_if_user_active(member_login):
                active = True
                return True
                break
            else:
                return False
    except:
        print "Transaction couldn't be completed, error getting communities data: " , ibm_db.stmt_errormsg()
        sys.exit(3)
# Query DB2 database
sql = "select DISTINCT COMMUNITY_UUID, NAME from sncomm.community;"
stmt = ibm_db.prepare(conn_comm, sql)
try:
    ibm_db.execute(stmt)
    while ibm_db.fetch_row(stmt) != False:
        community_id = ibm_db.result(stmt, 0)
        name = ibm_db.result(stmt, 1)
        if not check_community_owners(community_id):
            list =list + name + " ID: " + community_id + "\n"
            count  = count + 1
except:
    print "Transaction couldn't be completed, error getting communities: " , ibm_db.stmt_errormsg()
    sys.exit(3)

# Nagios standard feedback
if (count < int(args.warning)):
    print("Communites are OK, " + str(count) + " Communities without an owner: " + list.encode('utf-8') + "| Number of Communities=" +  str(count) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(0)
elif (count < int(args.critical)):
    print("Warning: " + str(count) + " Communities without an owner: "+ list.encode('utf-8') + "| Number of Communities=" +  str(count) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(1)
elif (count >= int(args.critical)):
    print("Critical: " + str(count) + " Communities without an owner!" + list.encode('utf-8') + "| Number of Communities=" +  str(count) + ";" + str(args.warning) + ";" + str(args.critical) + ";;")
    sys.exit(2)
else:
    print("UKNOWN number of Communities without an owner!")
    sys.exit(3)
