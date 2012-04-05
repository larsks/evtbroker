#!/usr/bin/python

import os
import sys
import argparse
import logging

import zmqevt.publisher

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--connect', '-c', default='tcp://localhost:13902')
    p.add_argument('--debug', action='store_true')
    p.add_argument('tag')
    p.add_argument('attrs', nargs='+')
    return p.parse_args()

def main():
    opts = parse_args()
    
    logging.basicConfig(
            level=logging.DEBUG if opts.debug else logging.INFO)
    logging.info('Publisher starting up.')

    attrs=dict([attr.split('=',1) for attr in opts.attrs])
    attrs['tag'] = opts.tag

    p = zmqevt.publisher.Publisher(
            pub_uri=opts.connect)

    p.publish(zmqevt.Event(attrs))

if __name__ == '__main__':
    main()

