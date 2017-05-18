#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

from kombu import Connection, Exchange


user = 'cpsrabbit'
passwd = 'canopsis'
host = '127.0.0.1'
port = 5672
vhost = 'canopsis'

conn = Connection('amqp://{0}:{1}@{2}:{3}/{4}'.format(user, passwd, host, port, vhost))
try:
    conn.connect()
    print(conn.connected)
    conn.release()
except socket.error, e:
    print("{0}".format(e))
