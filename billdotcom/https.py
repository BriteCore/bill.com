"""Wrapper for https auth. Uses requests."""

import requests
import xml.dom.minidom
from config import API_URL, get_logger
from exceptions import HTTPError, ServerResponseError

OK_CODES = [200]

def https_post(xmlstring):
    LOG = get_logger()

    response = requests.post(API_URL, data={'request': xmlstring})

    if response.status_code not in OK_CODES:
        message = "received HTTP {0}: {1} when sending to {2}: {3}".format(
                    response.status_code, response.text, API_URL, xmlstring
        )
        LOG.error(message)
        raise HTTPError(message)

    try:
        dom = xml.dom.minidom.parseString(response.text)
        status = dom.getElementsByTagName('status')[0].firstChild.data
    except:
        message = 'sent {0} got badly formatted reponse: {1}'.format(xmlstring, response.text)
        LOG.error(message)
        raise

    if status != 'OK':
        errorcode = dom.getElementsByTagName('errorcode')[0].firstChild.data
        errormessage = dom.getElementsByTagName('errormessage')[0].firstChild.data
        message = "server reponse: {0} {1} {2}".format(status, errorcode, errormessage)
        LOG.error(message)
        raise ServerResponseError(message)

    return dom

