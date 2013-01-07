#!/usr/bin/env python

from billdotcom import validate_config, Session

def main():
    validate_config()

    with Session() as s:
        accounts = s.get_list('chartofaccount')

    title = 'Got {0} chart of accounts:'.format(len(accounts))
    print title
    print '-'*len(title)

    print 'ID\t\t\tNumber\tName'
    print '-'*60
    for account in sorted(accounts, key=lambda x: x['accountNumber']):
        print '{id}\t{accountNumber}\t{name}'.format(**account)


if __name__=='__main__':
    main()

