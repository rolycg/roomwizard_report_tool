import csv
import io


def get_data(_file):
    with io.open(_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        return list(reader)[1:]
