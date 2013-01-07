#!/usr/bin/env python
from distutils.core import setup

setup(
    name='billdotcom',
    version='0.1.2',
    author='Amanda Quint, Matthew Thompson',
    author_email='amanda@britecore.com, matt@britecore.com',
    packages=['billdotcom'],
    scripts=[
        'bin/billdotcom_getorglist.py',
        'bin/billdotcom_getchartofaccounts.py',
        'bin/billdotcom_send_vendor_invite.py',
        'bin/billdotcom_set_external_id.py'
    ],
    url='https://github.com/IntuitiveWebSolutions/bill.com',
    license='LICENSE.txt',
    description='A client library for Bill.com in Python.',
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "iso8601",
    ],
)
