#!/usr/bin/env python

from billdotcom import validate_config, https_post, CONFIG

def main():
    validate_config()

    dom = https_post("""
        <request version="1.0" applicationkey="{appkey}">
        <getorglist>
            <username>{email}</username>
            <password>{password}</password>
        </getorglist>
        </request>
    """.format(**{key: value for (key, value) in CONFIG.items('authentication')}))

    org_infos = dom.getElementsByTagName('org_info')

    title = 'Got {0} organizations:'.format(len(org_infos))
    print title
    print '-'*len(title)

    for org in org_infos:
        name = org.getElementsByTagName('name')[0].firstChild.data
        orgid = org.getElementsByTagName('orgID')[0].firstChild.data
        print '{0}:\t{1}'.format(name, orgid)


if __name__=='__main__':
    main()

