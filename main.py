from parseCSV import get_data
from datetime import datetime
from room import Room
from pdf import convertHtmlToPdf


def fix_str(chain):
    return chain.strip().upper()


def convert_date(line, index):
    year, month, day = line[index].strip(), line[index + 1].strip(), line[index + 2].strip()
    hour, minute, second = line[index + 3].strip().split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


if __name__ == '__main__':
    data = get_data()
    info = []
    for line in data:
        info.append(Room(fix_str(line[1]), convert_date(line, 9), convert_date(line, 13), fix_str(line[17])))
    convertHtmlToPdf(info)
