#!/usr/bin/env bash
#
# Copyright (C) 2012 by Lele Long <schemacs@gmail.com>
# This file is free software, distributed under the GPL License.
#
# monitor cpu temperature
# in case of shutdown for high temp
#

THRESHOLD=40 # 80°C
SYS_FILE="/sys/class/thermal/thermal_zone0/temp"
TITLE="Your CPU is BURNNING!"

if [ ! -e "$SYS_FILE" ]; then
    echo "No thermal found: " $SYS_FILE
    exit 1
fi

while :
do
    raw_tmp=$(cat $SYS_FILE)
    tmp=$((raw_tmp / 1000 ))
    #tmp="${tmp%000}°C"
    if [ $tmp -gt $THRESHOLD ]; then
        echo "$tmp°C"
        #stock icon see http://developer.gnome.org/gtk/2.24/gtk-Stock-Items.html
        notify-send '$TITLE' "The cpu is burnning at $tmp°C" --icon=dialog-warning --expire-time=1000
    fi
    sleep 30
done

exit 0
