#!/bin/sh

echo "Starting Cron"
/usr/sbin/crond -n

echo "System is Ready"
tail -f /dev/null

