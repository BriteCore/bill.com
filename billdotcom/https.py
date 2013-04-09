"""Wrapper for https auth. Uses requests."""

import requests
import json
from config import API_URL, get_logger
from exceptions import HTTPError, ServerResponseError

OK_CODES = [200]

def get_status_and_message(data):
    '''Parse the status and error message (if applicable) from a JSON dict.

    Returns:
        Tuple of (status, message) where status is 'OK' or 'failed'.
    '''
    status = data['response_status']
    message = data['response_message']

    if status == 1:
        error_code = data['response_data']['error_code']
        error_message = data['response_data']['error_message']

        print data
        if not error_message:
            error_message = "NOCODE"

        message = "{0} {1} {2}".format(status, error_code, error_message)

    return (status, message)


def https_post(url, payload, params={}, ignore_status=False):
    '''Posts a data payload to Bill.com. It can optionally check for failed status.

    Args:
        payload (dict): A JSON compatible dict with data to send to bill.com's api.
        ignore_status (bool): If True, don't check for failed status codes.

    Returns:
        Dict of the JSON response.

    Raises:
        ServerReponseError
        HTTPError
    '''
    LOG = get_logger()

    api_url = API_URL + '/' + url

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    try:
        response = requests.post(api_url, params=params, data=payload, headers=headers)
    except Exception as e:
        raise ServerResponseError('Could not post to {0}: {1}'.format(api_url, e))

    if response.status_code not in OK_CODES:
        message = "received HTTP {0}: {1} when sending to {2}: {3}".format(
                    response.status_code, response.text, API_URL, payload
        )
        LOG.error(message)
        raise HTTPError(message)

    try:
        data = json.loads(response.text)
        status, message = get_status_and_message(data)
    except:
        message = 'sent {0} got badly formatted reponse: {1}'.format(payload, response.text)
        LOG.error(message)
        LOG.error("SENT TO {}: {}".format(response.url, payload))
        LOG.error("RECEIVED {}".format(data))
        raise

    if not ignore_status and status and status != 'OK':
        LOG.error(message)
        LOG.error("SENT TO {}: {}".format(response.url, payload))
        LOG.error("RECEIVED {}".format(data))
        raise ServerResponseError(message)

    return data['response_data']


