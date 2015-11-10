# check_connections_search_index.py
# Author: Klaus Bild
# E-Mail: klaus.bild@webgate.biz
#
# History:
# 20151110 kbild Initial release

#!/usr/bin/env python
import sys
import argparse
import urllib2
import cookielib
import urllib
import datetime
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='This script gets the arguments')
parser.add_argument('-H','--conn_host', help='Connections Domain',required=True)
parser.add_argument('-w','--warning',help='Warning value', required=True)
parser.add_argument('-c','--critical',help='Critical value ', required=True)
parser.add_argument('-u','--user',help='User ', required=True)
parser.add_argument('-p','--pw',help='Password ', required=True)
args = parser.parse_args()


password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://" + args.conn_host
password_mgr.add_password(None, top_level_url, args.user, args.pw)
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(urllib2.HTTPHandler, handler)
# Connect to IBM Connections site and get back a XML search result
soup = BeautifulSoup(opener.open('https://' + args.conn_host + '/search/atom/mysearch?scope=&query=test_something_weird&page=1&pageSize=10&format=light').read().strip(), "lxml")
# Get last update date and transform
search_date = datetime.datetime.strptime(soup.updated.string[:-10], "%Y-%m-%dT%H:%M:%S" )
if (datetime.datetime.now() - datetime.timedelta(hours=int(args.critical)) > search_date):
    print("Status Critical - Search Index older than " + args.critical + " hours - Search Index date " + str(search_date))
    sys.exit(1)
elif (datetime.datetime.now() - datetime.timedelta(hours=int(args.warning)) > search_date):
    print("Status Warning - Search Index older than " + args.warning + " hours - Search Index date " + str(search_date))
    sys.exit(2)
else:
    print("Status OK - Search Index date " + str(search_date))
    sys.exit(0)
