#!/usr/bin/env python

from billdotcom import validate_config, https_post, CONFIG
import json

def main():
    validate_config()

    auth = dict(CONFIG.items('authentication'))

    params = dict(
        userName = auth['email'],
        password = auth['password'],
        devKey = auth['appkey']
    )

    org_infos = https_post('ListOrgs.json', {}, params=params)

    title = 'Got {0} organizations:'.format(len(org_infos))
    print title
    print '-'*len(title)

    for org in org_infos:
        print '{orgId}\t{orgName}'.format(**org)


if __name__=='__main__':
    main()

