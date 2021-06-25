#!/bin/bash
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
SERVICE="celery"
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    #echo "$SERVICE service running, everything is fine"  | mail -s "測試信" yishanjob13@sapido.com.tw 
    #echo "$SERVICE service running, everything is fine"  | mail -s "$SERVICE is not running" yishanjob13@gmail.com
else
    #echo "$SERVICE is not running"
    echo "$SERVICE is not running"  | mail -s "緊急通知" yishanjob13@gmail.com
fi
#https://www.unix.com/shell-programming-and-scripting/135862-checking-see-if-service-running-shell-script.html
