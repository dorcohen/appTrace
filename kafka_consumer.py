#!/usr/bin/python

import re
import sys
import json
import time
import datetime
import urllib
import urllib2
import logging
from kafka import SimpleProducer, KafkaClient, KafkaConsumer

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


kafka = KafkaClient('16.125.104.60:9092')
producer = SimpleProducer(kafka)
producer.send_messages(b'picasso-apppulse', b'test message')


for t in kafka.topics:
    print("{0!r}:".format(t))
# To consume messages
consumer = KafkaConsumer('picasso-apppulse',
                         group_id='my_group',
                         bootstrap_servers=['16.125.104.60:9092'])
for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))