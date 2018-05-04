import sys
import os
import re

import requests
from flask import Flask, request
from flask_json import FlaskJSON, as_json, JsonError

VOIP_NUMBER = os.environ['VOIP_NUMBER']
OUTGOING_VOIP_PASSWORD = os.environ['OUTGOING_VOIP_PASSWORD']

app = Flask(__name__)
FlaskJSON(app)

app.config['JSON_ADD_STATUS'] = False


class AuthenticationError(RuntimeError):
    pass


@app.route('/api/v1/send/', methods=['POST'])
@as_json
def index():
    validate_authorization_header(request.headers.get('authorization'))

    post_data = request.get_json()

    destination = validate_destination(post_data.get('destination'))
    message = validate_message(post_data.get('message'))

    try:
        response = send_sms(destination, message)

    except AuthenticationError:
        raise JsonError(
            status=403,
            message=(
                'AAISP API returned authentication failure, check the '
                'configured VOIP_NUMBER and OUTGOING_VOIP_PASSWORD'
            )
        )

    return {
        'message': 'Response from sms.aa.net.uk/sms.cgi: {}'.format(response)
    }


def validate_authorization_header(header):
    match = re.match('[Bb]earer (?P<token>.+)', header) if header else None

    if header is None or match is None:
        raise JsonError(
            status=403,
            message=(
                'Please provide the header: `Authorization: Bearer <token>` '
                'matching a token configured in `API_TOKENS`'
            )
        )

    token_ok = match.group('token') in load_api_tokens()

    if not token_ok:
        raise JsonError(
            status=400,
            message=(
                'Bad API token, please check `API_TOKENS`'
            )
        )

    else:
        return True


def load_api_tokens():
    pairs = os.environ['API_TOKENS'].split(',')

    return [pair.split(':')[1] for pair in pairs]


def validate_destination(destination):
    if destination is None:
        raise JsonError('Missing field `destination`')

    return destination


def validate_message(message):
    if message is None:
        raise JsonError('Missing field `message`')

    return message


def main(argv):
    send_sms(
        argv[1],
        argv[2]
    )


def send_sms(destination, message):
    """
    On success, return the raw message from the CGI endpoint.
    On failure, return a requests.exceptions.RequestError appropriate to the
    error (note that AAISP always returns HTTP 200, even for errors :\)
    """

    response = requests.post(
        "https://sms.aa.net.uk/sms.cgi",
        data={
            'username': VOIP_NUMBER,
            'password': OUTGOING_VOIP_PASSWORD,
            'destination': destination,
            'message': message,
        }
    )
    response.raise_for_status()  # allow this to bubble right up

    text = response.text

    if text.startswith('ERR:'):
        raise make_appropriate_exception(text[4:].strip())

    elif text.startswith('OK:'):
        print('HTTP {} : {}'.format(response.status_code, response.text))
        return text

    else:
        raise RuntimeError('Unexpected response text `{}`'.format(text))


def make_appropriate_exception(error_message):
    if error_message == 'Authentication failed':
        return AuthenticationError()

    return RuntimeError('Unrecognised response: `{}`'.format(error_message))


if __name__ == '__main__':
    main(sys.argv)
