import requests
import datetime
import StringIO
import zipfile
import os

IPS = ('http://10.10.7.50', 'http://10.10.7.51')
URL = '/admin/test/GetRoomUsage.action'
COOKIES = {
    'http://10.10.7.50': 'd8njr06y33uc17thmiuizz6rb',
    'http://10.10.7.51': '7zu982q1ohzspqmf60gzbvx6'
}



FILE_NAME = 'rwusagereport.csv'

HEADERS = {
    'http://10.10.7.51': {
        'Host': '10.10.7.51',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://10.10.7.51/admin/test/GetRoomUsage.action',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'JSESSIONID=7zu982q1ohzspqmf60gzbvx6; JSESSIONID=7zu982q1ohzspqmf60gzbvx6'
    },
    'http://10.10.7.50': {
        'Host': '10.10.7.50',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://10.10.7.50/admin/test/GetRoomUsage.action',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'JSESSIONID=d8njr06y33uc17thmiuizz6rb; JSESSIONID=d8njr06y33uc17thmiuizz6rb'
    }
}


def get_reports(date_in, date_out):
    payload = {
        'startDay': str(date_in.day),
        'startMonth': str(date_in.month),
        'startYear': str(date_in.year),
        'endDay': str(date_out.day),
        'endMonth': str(date_out.month),
        'endYear': str(date_out.year),
        'roomUsage': 'usedates',
        'detailed': 'detailed',
        'format': 'CSV'
    }

    for address in IPS:
        r = requests.post(address + URL, data=payload, headers=HEADERS[address])

        # with open(FILE_NAME + address[-2:] + '.zip', 'w+') as f:
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        z.extractall()
        os.rename(FILE_NAME, 'report_' + address[-2:] + '.csv')


# get_reports(date_in=datetime.datetime(2017, 1, 1), date_out=datetime.datetime.now())
