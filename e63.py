#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Copyright (C) 2012 by Lele Long <schemacs@gmail.com>
This file is free software, distributed under the GPL License.

This file is for my e63 cellphone.

http://www.developer.nokia.com/Community/Wiki/Python_on_Symbian
http://www.developer.nokia.com/Community/Wiki/Python_on_Symbian/03._System_Information_and_Operations
http://pys60.garage.maemo.org/doc/s60/module-contacts.html
http://pys60.garage.maemo.org/doc/s60/node83.html

'''
import socket
import datetime
import urllib

# import appuifw
import e32
import telephone
import contacts
import inbox
import logs

DEFAULT_AP = u'GGG'
# the web handler for message forwarding
URL = 'http://www.schemacs.com:5000/forward'
KEY = 'YOUR-KEY-HERE'

app_lock = e32.Ao_lock()
box = inbox.Inbox()

# http://www.developer.nokia.com/Community/Wiki/Python_on_Symbian/09._Basic_Network_Programming#Access_point_selection
socket.set_default_access_point(DEFAULT_AP)


def notify(message):
    print 'notify', message
    playload = {'key': KEY,
                'message': message.encode('utf8')}
    params = urllib.urlencode(playload)
    remote_fh = urllib.urlopen(URL, params)
    result = remote_fh.read()
    return result


def on_message(message_id):
    # http://www.developer.nokia.com/Community/Wiki/How_read_SMS_in_the_inbox
    # appuifw.note(u'A new message:\n %s' % box.content(message_id))
    message = (u'[%s] sms from %s: %s' %
               (datetime.datetime.fromtimestamp(int(box.time(message_id))),
               box.address(message_id), box.content(message_id)))
    notify(message)
    #app_lock.signal()


def on_call(stateInformation):
    # http://www.developer.nokia.com/Community/Wiki/Python_on_Symbian/06._Telephony_and_Messaging
    newState = stateInformation[0]
    if newState == telephone.EStatusRinging:
        phone = stateInformation[1]
        message = u'[%s] call from %s' % (datetime.datetime.now().replace(microsecond=0), phone)
        notify(message)


def retrieve_contacts():
    db = contacts.open()
    fh = open('E:\data\python\contacts.txt', 'w')
    fh.write(db.export_vcards(db.keys()))
    fh.close()
    for contact in db.find(''):
        fields = ['first_name', 'last_name', 'mobile_number']
        find_values = [contact.find(field) for field in fields]
        values = [field_values[0].value if field_values else '' for field_values in find_values]
        print contact.id,
        for value in values:
            print value,
        print


def retrieve_sms():
    message_ids = box.sms_messages()  # all message ID's
    fh = open('E:\data\python\sms.txt', 'w')
    for message_id in message_ids:
        content_escaped = box.content(message_id).replace(u'\n', u'\\n')
        record = [unicode(box.time(message_id)), box.address(message_id), content_escaped]
        fh.write((u'\t'.join(record) + u'\n').encode('utf8'))
    fh.close()


def print_log(log):
    fh = open('E:\data\python\call-logs.txt', 'a')
    fields = ['number', 'name', 'description', 'direction', 'status', 'subject',
              'id', 'contact', 'duration', 'duration type', 'flags', 'link', 'time', 'data']
    values = [unicode(log[field]) for field in fields]
    fh.write((u'\t'.join(values) + '\n').encode('utf8'))
    for field in fields:
        print log[field],
    print


def do_retrieve_logs(log_type, mode):
    if log_type == 'call':
        for call in logs.calls():
            #print call['number'], call['duration']
            print_log(call)
    elif log_type == 'sms':
        for message in logs.sms():
            #print message['number'], message['subject'], message['time']
            #print_log(message)
            pass
    else:
        print 'Unknown log type and mode', log_type, mode


def retrieve_logs():
    log_types = ['call', 'sms', 'data', 'fax', 'email', 'scheduler']
    modes = ['in', 'out', 'fetched', 'missed', 'in_alt', 'out_alt']
    for log_type in log_types:
        for mode in modes:
            do_retrieve_logs(log_type, mode)


def main():
    #retrieve_contacts()
    #retrieve_sms()
    #retrieve_logs()
    # bind inbox to new message event
    box.bind(on_message)
    telephone.incoming_call()
    # bind incomming calls to on_call
    telephone.call_state(on_call)
    print 'waiting for message and calls....'
    # Wait for Exit
    app_lock.wait()


if __name__ == '__main__':
    main()
