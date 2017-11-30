from parseCSV import get_data
from datetime import datetime
from room import Room, RoomOffice
from pdf import convertHtmlToPdf, outputFilename
from difflib import SequenceMatcher
from email_util import send_email_with_attachment
from find_reports import get_reports
import os
from threading import Timer

names = []
times = {}
timeout = 10.0  # Sixty seconds

ROOMS = {
    '50': 'Room A',
    '51': 'Room B'
}


def similar(text, other_text):
    return SequenceMatcher(None, text, other_text).ratio()


def fix_str(chain):
    global names, times
    chain = chain.strip().upper()
    try:
        times[chain] += 1
    except:
        times[chain] = 1
    for x in names:
        if similar(x, chain) >= 0.9:
            chain = x
            break
    names.append(chain)
    names = list(set(names))
    return chain


def convert_date(line, index):
    year, month, day = line[index].strip(), line[index + 1].strip(), line[index + 2].strip()
    hour, minute, second = line[index + 3].strip().split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


def get_room(filename):
    if '50' in filename:
        return RoomOffice.get_name_room(RoomOffice._50)
    elif '51' in filename:
        return RoomOffice.get_name_room(RoomOffice._51)


def get_american_date(date):
    return date.strftime('%m/%d/%Y')


def _main(date_in, date_out):
    global names
    global times
    get_reports(date_in, date_out)
    files = os.listdir('.')
    files = filter(lambda x: '.csv' in x, files)
    for _file in files:
        data = get_data(_file)
        info = {}
        names = []
        times = {}
        count = 0
        _room = get_room(_file)
        for line in data:
            info[count] = Room(count, fix_str(line[1]), convert_date(line, 9), convert_date(line, 13),
                               fix_str(line[17]))
            count += 1
        convertHtmlToPdf(info, start_date=get_american_date(date_in), end_date=get_american_date(date_out),
                         letter=_room)
        pdf = _room + outputFilename
        send_email_with_attachment(pdf, _room)
        os.remove(pdf)
        os.remove(_file)


def job_function():
    print("Running report function")
    today = datetime.today()
    _main(datetime(today.year, today.month - 1, today.day), today)
    Timer(60 * 60 * 24, job_function).start()


if __name__ == '__main__':
    job_function()
