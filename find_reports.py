import requests

IPS = ('', '')
URL = ''
COOKIES = {
    '': ''
}

FILE_NAME = 'report_'


def get_reports():
    for address in IPS:
        r = requests.post(address + URL, data={}, headers={}, cookies=COOKIES)
        with open(FILE_NAME + address, 'a+w') as f:
            f.write(r.content)
