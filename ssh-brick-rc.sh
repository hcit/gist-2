#!/usr/bin/env bash
#
# Copyright (C) 2013 by Lele Long <schemacs@gmail.com>
# This file is free software, distributed under the GPL License.
#
# notify when someone unexpected login machine
# this script only just report it to /ssh_brick endpoint
# which will do checking on it.
#
# see /etc/profile and /etc/ssh/sshrc
#
# SSH_CLIENT='192.168.223.17 36673 22'
# SSH_CONNECTION='192.168.223.17 36673 192.168.223.229 22'
# SSH_TTY=/dev/pts/6

ENDPOINT=http://labs.schemacs.com:5000/ssh_brick 
source secrets.sh
KEY="${AUTH_KEYS[ssh-brick]}"

# /etc/profile
if [ -n "$SSH_CLIENT" ]; then
   curl --fail --silent -d key="$KEY" -d ssh_connection="$SSH_CONNECTION" $ENDPOINT >/dev/null
   #ip=`echo $SSH_CONNECTION | cut -d " " -f 1`
   text="$(date): ssh login to ${USER}@$(hostname -f)”
   text=”$text from $(echo $SSH_CLIENT|awk '{print $1}')"
   #logger -t ssh-wrapper -p info.warn $USER login from $ip
   #echo "$TEXT" | sendemail -q -u "SSH Login" -f "Originator <from@address.com>" -t "<you@you.domain>" -s smtp.server.com
   ##echo $TEXT|mail -s "ssh login" you@your.domain
fi

#NOTE this will exit the SHELL AND SSH CONNECTION
#exit 0
