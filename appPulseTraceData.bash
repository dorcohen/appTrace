#!/bin/bash 
USER_NAME="apm@hp.com"
PASSWORD=""
MACHINE="http://myd-vm18577.hpswlabs.adapps.hp.com:8080"
APPLICATION_ID="7d38ccf63efc445591097537dd7b2b33"
TODAY=$(date -d "today" +%s%3N)
MONTH_AGO=$(date -d "month ago" +%s%3N)
TIMEZONE="Asia/Jerusalem"

echo "LOGIN WITH USER NAME : "$USER_NAME"";

TENANTID=$(curl -L -X POST -H 'Content-Type:application/json' -H 'Accept-Encoding: gzip, deflate, sdch' -d '{"loginName":"'$USER_NAME'","password": "'$PASSWORD'"}' -c "cookie.txt" -s $MACHINE/apmappsSaasMock/rest/saasportalmock/login | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["tenantId"]');

curl -b "cookie.txt" -c "cookie.txt" -s $MACHINE/apmappsDiag/index.html > /dev/null;

echo "SAVING AUTH COOKIES";

XSRF_TOKEN=$(cat cookie.txt | grep XSRF-TOKEN| cut -f7);

echo "GETTING APPLICATIONS DATA";

APPLICATIONS=$(curl -b "cookie.txt" -H "X-XSRF-TOKEN:"$XSRF_TOKEN"" -o trace_applications.log -s $MACHINE/apmappsDiag/rest/admin/applications?TENANTID=$TENANTID);

echo "GETTING APPLICATION ID "$APPLICATION_ID" DATA";

TRANSACTIONS=$(curl -b "cookie.txt" -H "X-XSRF-TOKEN:"$XSRF_TOKEN"" -o trace_transactions.log -s "$MACHINE/apmappsDiag/rest/transactionHealthReports/transactionsSummary/applications/$APPLICATION_ID?from="$MONTH_AGO"&to="$TODAY"&timeView=pastMonth&orderBy=mostTimeConsuming&granularity=86400000&timeZone="$TIMEZONE"&TENANTID="$TENANTID"");

