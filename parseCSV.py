import csv


def get_data():
    with open('rwusagereport.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        return list(reader)[1:]
