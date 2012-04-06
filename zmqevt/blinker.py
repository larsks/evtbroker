#!/usr/bin/python

import logging
import threading
import time

class Blinker (object):
    def __init__ (self, path):
        self.path = path
        self.active = False
        self.log = logging.getLogger('zmqevt.blinker')
        self.log.info('Blinker created on %s' % self.path)

        self.on_interval=1
        self.off_interval=0.5

    def on(self):
        if not self.active:
            self.log.info('Activate blinker.')
            self.active = True
            self.t = threading.Thread(target=self.blink)
            self.t.start()

    def blink(self):
        while self.active:
            self.fd = open(self.path)
            time.sleep(self.on_interval)
            self.fd.close()
            time.sleep(self.off_interval)

    def off(self):
        if self.active:
            self.log.info('Deactivate blinker.')
            self.active = False
            self.t.join()

