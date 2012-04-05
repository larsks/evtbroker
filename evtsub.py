#!/usr/bin/python

import os
import sys
import argparse
import logging

from zmq.eventloop import ioloop

from zmqevt.subscriber import Subscriber

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--connect', default='tcp://localhost:13903')
    p.add_argument('--debug', action='store_true')
    p.add_argument('patterns', nargs='*', default=[''])
    return p.parse_args()

def printmsg(evt):
    print 'EVENT:', evt

def main():
    opts = parse_args()

    logging.basicConfig(
            level=logging.DEBUG if opts.debug else logging.INFO)
    logging.info('Subscriber starting up.')

    s = Subscriber(sub_uri=opts.connect, patterns=opts.patterns)
    s.register_callback(printmsg)

    ioloop.install()
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()


