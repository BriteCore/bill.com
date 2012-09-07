"""Wrapper for https auth. Uses requests."""

import requests
import xml.dom.minidom
from config import API_URL, get_logger
from exceptions import HTTPError, ServerResponseError

OK_CODES = [200]

def get_status_and_message(node):
    '''Parse the status and error message (if applicable) from an XML node.

    Returns:
        Tuple of (status, message) where status is 'OK' or 'failed'.
    '''
    # status = node.getElementsByTagName('status')
    status = [x for x in node.childNodes if x.nodeType == xml.dom.Node.ELEMENT_NODE and x.tagName == "status"]
    message = None

    if status:
        status = status[0].firstChild.data

        if status != 'OK':
            errorcode = node.getElementsByTagName('errorcode')
            if errorcode:
                errorcode = errorcode[0].firstChild.data
            else:
                errorcode = "NOCODE"
            errormessage = node.getElementsByTagName('errormessage')[0].firstChild.data
            message = "{0} {1} {2}".format(status, errorcode, errormessage)

    return (status, message)


def https_post(xmlstring, ignore_status=False):
    '''Posts an XML string to Bill.com. It can optionally check for failed status.

    Args:
        xmlstring (str): An XML document string.
        ignore_status (bool): If True, don't check for failed status codes.

    Returns:
        XML DOM object.

    Raises:
        ServerReponseError
        HTTPError
    '''
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
        status, message = get_status_and_message(dom)
    except:
        message = 'sent {0} got badly formatted reponse: {1}'.format(xmlstring, response.text)
        LOG.error(message)
        raise

    if not ignore_status and status and status != 'OK':
        LOG.error(message)
        raise ServerResponseError(message)

    return dom


def https_post_operation(xmlstring):
    '''Posts an XML string containing one or more operations to Bill.com.
    It will sort successful and failed operations separately.

    Args:
        xmlstring (str): An XML document string.

    Returns:
        A dict formatted like this:
            'OK': { 'transaction1': dom1, 'transaction2': dom2 },
            'failed': { 'transaction3': { 'status':'failed', 'message':'some error' } }

    Raises:
        ServerResponseError
        HTTPError
    '''
    dom = https_post(xmlstring, ignore_status=True)

    operations = dom.getElementsByTagName('operationresult')

    result = {
        'OK': {},
        'failed': {}
    }

    for operation in operations:
        transaction = operation.getAttribute('transactionId')
        status, message = get_status_and_message(operation)

        if status and status != 'OK':
            result['failed'][transaction] = {'status':status, 'message':message}
        else:
            result['OK'][transaction] = operation

    return result

