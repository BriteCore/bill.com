#!/usr/bin/env python

from billdotcom import validate_config, Session
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Set the external id for a Bill.com object.')
    parser.add_argument('object_id', type=str, help='A Bill.com object id.')
    parser.add_argument('external_id', type=str, help='The external id to set.')

    args = parser.parse_args()

    validate_config()

    with Session() as s:
        s.set_external_id(args.object_id, args.external_id)
        print('set external id on object {0} to {1}'.format(args.object_id, args.external_id))
