#!/usr/bin/env python

from billdotcom import validate_config, Vendor, Session

def main():
    validate_config()

    with Session() as s:
        vendor = Vendor(name=raw_input('Vendor name: '))
        vendor['id'] = s.create_vendor(vendor)

        print 'Successfully created vendor "{0}" with id {1}'.format(vendor['name'], vendor['id'])

        s.send_vendor_invite(vendorId=vendor['id'], email=raw_input('Vendor email: '))

        print 'Emailed vendor invite.'


if __name__=='__main__':
    main()

