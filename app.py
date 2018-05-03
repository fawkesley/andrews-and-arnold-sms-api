import datetime
import sys
import os

import requests
from flask import Flask
from flask_json import as_json

VOIP_NUMBER = os.environ['VOIP_NUMBER']
OUTGOING_VOIP_PASSWORD = os.environ['OUTGOING_VOIP_PASSWORD']

app = Flask(__name__)


@app.route('/api/v1/send/')
@as_json
def index():
    return 'Hello, World!'


def main(argv):
    send_sms(
        argv[1],
        argv[2]
    )


def send_sms(destination, message):
    response = requests.post(
        "https://sms.aa.net.uk/sms.cgi",
        data={
            'username': VOIP_NUMBER,
            'password': OUTGOING_VOIP_PASSWORD,
            'destination': destination,
            'message': message,
        }
    )
    response.raise_for_status()
    print('HTTP {} : {}'.format(response.status_code, response.text))
    # Note: HTTP code *always* 200, but response.text starts with 'ERR:' or 'OK:'


if __name__ == '__main__':
    main(sys.argv)
