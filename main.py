from parseCSV import get_data
from datetime import datetime
from room import Room
from pdf import convertHtmlToPdf, outputFilename
from difflib import SequenceMatcher
from email_util import send_email_with_attachment
import os



names = []
times = {}


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


if __name__ == '__main__':
    data = get_data()
    info = {}
    names = []
    times = {}
    count = 0
    for line in data:
        info[count] = Room(count, fix_str(line[1]), convert_date(line, 9), convert_date(line, 13), fix_str(line[17]))
        count += 1
    convertHtmlToPdf(info, start_date='01/01/2017', end_date='11/15/2017', letter="Room A")
    send_email_with_attachment(outputFilename)
    os.remove(outputFilename)
