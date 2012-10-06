import argparse
import sys

from os import environ

import aquino

CONSUMER_KEY = (environ['CONSUMER_KEY']
        if 'CONSUMER_KEY' in environ else 'consumer_key')
CONSUMER_SECRET = (environ['CONSUMER_SECRET']
        if 'CONSUMER_SECRET' in environ else 'consumer_secret')

AQAPI_PORT = (environ['AQAPI_PORT']
        if 'AQAPI_PORT' in environ else 443)
AQAPI_DOMAIN = (environ['AQAPI_DOMAIN']
        if 'AQAPI_DOMAIN' in environ else 'aquino.com')
AQAPI_PROTOCOL = (environ['AQAPI_PROTOCOL']
        if 'AQAPI_PROTOCOL' in environ else 'https')


parser = argparse.ArgumentParser(description='Command line Marketplace client')
parser.add_argument('method', type=str, help='command to be run on arguments',
        choices=['listen',])
parser.add_argument('attrs', metavar='attr', type=str, nargs='*',
        help='arguments')

args = parser.parse_args()

kwargs = {}
max_count = None
if args.attrs:
    max_count = args.attrs.pop(0)
    if args.attrs:
        kwargs['serial_port'] = args.attrs.pop(0)


board = aquino.Aquino(CONSUMER_KEY, CONSUMER_SECRET, **kwargs)
board.listen(max_count)
