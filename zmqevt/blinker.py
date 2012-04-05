#!/usr/bin/python

import logging

class Blinker (object):
    def __init__ (self, path):
        self.path = path
        self.active = False
        self.log = logging.getLogger('zmqevt.blinker')
        self.log.info('Blinker created on %s' % self.path)

    def on(self):
        if not self.active:
            self.log.info('Activate blinker.')
            self.fd = open(self.path)
            self.active = True

    def off(self):
        if self.active:
            self.log.info('Deactivate blinker.')
            self.fd.close()
            self.active = False

