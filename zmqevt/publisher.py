#!/usr/bin/python

import logging

import zmq
from zmq.eventloop.zmqstream import ZMQStream

import defaults
import event

class Publisher (object):
    def __init__(self,
            pub_uri=defaults.publisher_pub_uri,
            ):

        self.pub_uri = pub_uri
        
        self.setup_logging()
        self.setup_zmq()
        self.setup_sockets()

    def setup_logging(self):
        self.log = logging.getLogger('zmqevt.publisher')

    def setup_zmq(self):
        self.context = zmq.Context()

    def setup_sockets(self):
        self.pub = self.context.socket(zmq.PUB)
        self.pub.connect(self.pub_uri)

    def publish(self, evt):
        self.log.debug('Send: %s' % (str(evt.dump())))
        self.pub.send_multipart(evt.dump())

