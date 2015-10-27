#!/usr/bin/python

import re
import sys
import json
import time
import datetime
import urllib
import urllib2

#for i in range(100):
#    time.sleep(1)
#    sys.stdout.write("\r%d%%" % i)
#    sys.stdout.flush()

#COLORS
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

username = raw_input('ENTER USER NAME[apm@hp.com]') or "apm@hp.com"
password = raw_input('ENTER PASSWORD[]') or ""
machine  = raw_input('ENTER MACHINE[http://myd-vm18577.hpswlabs.adapps.hp.com:8080]') or "http://myd-vm18577.hpswlabs.adapps.hp.com:8080"
timezone = raw_input('ENTER TIMEZONE[Asia/Jerusalem]') or "Asia/Jerusalem"

#REST API
login_url = machine + "/apmappsSaasMock/rest/saasportalmock/login"
index_url = machine + "/apmappsDiag/index.html"
applications_url = machine + "/apmappsDiag/rest/admin/applications"
transactions_url = machine + "/apmappsDiag/rest/transactionHealthReports/transactionsSummary/applications/"


today = int(round(time.mktime(datetime.datetime.now().timetuple()) * 1000));
month_ago = int(round(time.mktime((datetime.datetime.now()-datetime.timedelta(days=30)).timetuple()) * 1000));

#-----------------LOGIN--------------------
print "LOGIN WITH USER NAME : %s " % (username)

url = login_url
payload = { "loginName": username, "password": password }
headers = { 'Accept-Encoding': 'gzip, deflate, sdch','Content-Type': 'application/json'  }
data = json.dumps(payload)#urllib.urlencode(payload)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)

if response.getcode() == 200:
    print OKGREEN+"SUCCESS"+ENDC
    login__cookie = response.info()['Set-Cookie']
    tenantId = json.loads(response.read())['tenantId']

#-----------------XSRF--------------------
print "GETTING XSRF TOKEN"

url = index_url
headers = { 'Cookie' :  login__cookie }
req = urllib2.Request(url, "", headers)
response = urllib2.urlopen(req)

if response.getcode() == 200:
    print OKGREEN+"SUCCESS"+ENDC
    xsrf__cookie = response.info()['Set-Cookie']
    xsrf_token = xsrf__cookie.split('=')[1];

#-----------------APPLICATIONS--------------------    
print "GETTING ALL TENANT ID %s APPLICATIONS" %(tenantId)

url = applications_url +"?TENANTID="+ str(tenantId)
req = urllib2.Request(url)
req.add_header('X-XSRF-TOKEN', str(xsrf_token))
req.add_header('Cookie' , str(xsrf__cookie) +"; "+ str(login__cookie))
httpHandler = urllib2.HTTPHandler()
#httpHandler.set_http_debuglevel(1)
opener = urllib2.build_opener(httpHandler)
response = opener.open(req)

if response.getcode() == 200:
    print OKGREEN+"SUCCESS"+ENDC
    applications = json.loads(response.read())
    
for application in applications['applications']:
    print BOLD +"APP_NAME : "+ ENDC + OKBLUE + application['appName'] + ENDC + BOLD + "  APP_ID : " + ENDC + OKBLUE + application['appId'] + ENDC
    
app_id = raw_input('ENTER SELECTED APPLICATION ID['+applications['applications'][0]['appId']+']') or applications['applications'][0]['appId']

#-----------------TRANSACTIONS--------------------
print "GETTING APPLICATION ID %s TRANSACTIONS" %(app_id)

url = transactions_url + str(app_id) +"?TENANTID="+ str(tenantId) +"&from=" + str(month_ago) + "&to=" +str(today)+ "&timeZone=" +str(timezone)+ "&timeView=pastMonth&orderBy=mostTimeConsuming&granularity=86400000"
req = urllib2.Request(url)
req.add_header('X-XSRF-TOKEN', str(xsrf_token))
req.add_header('Cookie' , str(xsrf__cookie) +"; "+ str(login__cookie))
httpHandler = urllib2.HTTPHandler()
opener = urllib2.build_opener(httpHandler)
response = opener.open(req)

if response.getcode() == 200:
    print OKGREEN+"SUCCESS"+ENDC
    transactions = json.loads(response.read())

for transaction in transactions['responseList']:
    print BOLD +"TRANSACTION_NAME : "+ ENDC + OKBLUE + str(transaction['transactionName'])  + ENDC + BOLD + "  RESPONSE_TIME : "+ ENDC + OKBLUE + str(transaction['responseTime']) + ENDC + BOLD + "  THROUGHPUT : "+ ENDC + OKBLUE + str(transaction['throughput']) + ENDC + BOLD +"  TIME_CONSUMING : "+ ENDC + OKBLUE + str(transaction['timeConsuming']) + ENDC