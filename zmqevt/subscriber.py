#!/usr/bin/python

import logging

import zmq
from zmq.eventloop.zmqstream import ZMQStream

import defaults
import event

class Subscriber (object):
    def __init__(self,
            sub_uri=defaults.subscriber_sub_uri,
            patterns=None,
            callbacks=None,
            ):

        self.sub_uri = sub_uri
        
        if patterns:
            self.patterns = patterns
        else:
            self.patterns = []

        if callbacks:
            self.callbacks = callbacks
        else:
            self.callbacks = []
        
        self.setup_logging()
        self.setup_zmq()
        self.setup_sockets()
        self.setup_subscriptions()
        self.setup_events()

    def setup_logging(self):
        self.log = logging.getLogger('zmqevt.subscriber')

    def setup_zmq(self):
        self.context = zmq.Context()

    def setup_sockets(self):
        self.sub = ZMQStream(self.context.socket(zmq.SUB))
        self.sub.connect(self.sub_uri)

    def setup_subscriptions(self):
        if self.patterns:
            for p in self.patterns:
                self.subscribe(p)

    def subscribe(self, pattern):
        self.log.debug('Subcribe to "%s".' % pattern)
        self.sub.setsockopt(zmq.SUBSCRIBE, pattern)

    def setup_events(self):
        self.sub.on_recv(self.on_recv)

    def register_callback(self, func, data=None):
        self.callbacks.append((func,data))

    def unregister_callback(self, func):
        self.callbacks = [x for x in self.callbacks if x[0] is not func]

    def on_recv(self, msg):
        self.log.debug('Receive: %s' % (str(msg)))

        assert len(msg) == 2, 'Received invalid message.'

        # This regenerates the event to ensure that we don't
        # pass on invalid data.
        try:
            evt = event.Event.load(msg)
        except Exception, detail:
            self.log.error('Error processing message: %s' % detail)
            return

        self.log.debug('Event: %s' % (str(evt.dump())))

        for func, data in self.callbacks:
            func(evt, data=data)

