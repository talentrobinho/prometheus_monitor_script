#!/bin/bash
[[ $# -ne 2 ]] && echo "restart fail[param err]" && exit 1
pidfile="monitor_ws_$1_$2.pid"
[[ ! -f $pidfile ]] && echo "$pidfile is not exist" && exit 1 
kill $(cat $pidfile)
