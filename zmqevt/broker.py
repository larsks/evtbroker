#!/usr/bin/python

import logging

import zmq
from zmq.eventloop.zmqstream import ZMQStream

import defaults
import event

class Broker (object):
    def __init__(self,
            pub_uri=defaults.broker_pub_uri,
            sub_uri=defaults.broker_sub_uri,
            patterns=None,
            ):

        self.pub_uri = pub_uri
        self.sub_uri = sub_uri
        
        if patterns:
            self.patterns = patterns
        else:
            self.patterns = []
        
        self.setup_logging()
        self.setup_zmq()
        self.setup_sockets()
        self.setup_subscriptions()
        self.setup_events()

    def setup_logging(self):
        self.log = logging.getLogger('zmqevt.broker')

    def setup_zmq(self):
        self.context = zmq.Context()

    def setup_sockets(self):
        self.sub = ZMQStream(self.context.socket(zmq.SUB))
        self.sub.bind(self.sub_uri)

        self.pub = ZMQStream(self.context.socket(zmq.PUB))
        self.pub.bind(self.pub_uri)

    def setup_subscriptions(self):
        if self.patterns:
            for p in self.patterns:
                self.subscribe(p)

    def subscribe(self, pattern):
        self.log.debug('Subcribe to "%s".' % pattern)
        self.sub.setsockopt(zmq.SUBSCRIBE, pattern)

    def setup_events(self):
        self.sub.on_recv(self.publish)

    def publish(self, msg):
        assert len(msg) == 2, 'Received invalid message.'

        # This regenerates the event to ensure that we don't
        # pass on invalid data.
        try:
            evt = event.Event.load(msg)
        except Exception, detail:
            self.log.error('Error processing message: %s' % detail)
            return

        self.log.debug('Event: %s' % (str(evt.dump())))
        self.pub.send_multipart(evt.dump())

