#!/bin/bash
[[ $# -ne 2 ]] && echo "restart fail[param err]" && exit 1
#pidfile="monitor_consume_new_$1_$2.pid"
#[[ ! -f $pidfile ]] && echo "$pidfile is not exist" && exit 1 
#kill $(cat $pidfile)
#sleep 3
python monitor_ws.py $1 $2 >> /tmp/monitor_ws.log 2>&1 &

