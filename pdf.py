from xhtml2pdf import pisa
import os
from datetime import datetime

beginHtml = "<html><body>"
endHtml = "</body></html>"
outputFilename = "test.pdf"


def generate_row(row):
    res = "<tr>"
    res += '<td>' + row.office + '</td>'
    res += '<td>' + str(row.start_date.strftime("%m/%d/%y %H:%M:%S")) + '</td>'
    res += '<td>' + str(row.end_date.strftime("%m/%d/%y %H:%M:%S")) + '</td>'
    res += '<td>' + row.host + '</td>'
    res += "</tr>"
    return res


def generate_resume_row(data):
    res = ''
    for x in data.keys():
        for y in data[x].keys():
            res += "<tr>"
            res += '<td>' + str(x) + '</td>'
            res += '<td>' + str(data[x][y]) + '</td>'
            res += '<td>' + str(y) + '</td>'
            res += "</tr>"
    return res


def generate_header(fields):
    res = "<tr>"
    for field in fields:
        res += '<th align="left">' + field + '</th>'
    res += "</tr>"
    return res


def get_hours(start, end):
    elapsed = end - start
    return elapsed.seconds // 3600


def convert_resume_data(rooms):
    data = {}
    for room in rooms:
        office_hour = data.get(room.host)
        if office_hour:
            hour = office_hour.get(room.office)
            if hour:
                office_hour[room.office] += get_hours(room.start_date, room.end_date)
            else:
                office_hour[room.office] = get_hours(room.start_date, room.end_date)
        else:
            data[room.host] = {room.office: get_hours(room.start_date, room.end_date)}
    return data


def convertHtmlToPdf(room):
    rows = ""
    for r in room:
        rows += generate_row(r)

    header = generate_header(('OFFICE', 'START DATE', 'END DATE', 'HOST'))
    table = '<table>' + header + rows + '</table>'
    header_resume = generate_header(('HOST', 'HOURS', 'OFFICE'))
    rows_resume = generate_resume_row(convert_resume_data(room))
    resume = '<table>' + header_resume + rows_resume + '</table>'
    jump = '<p style="page-break-after: always;">&nbsp;</p>'

    source_html = beginHtml + resume + jump + table + endHtml
    result_file = open(outputFilename, "w+b")

    pisaStatus = pisa.CreatePDF(
        source_html,  # the HTML to convert
        dest=result_file)  # file handle to recieve result
    # close output file
    result_file.close()  # close output file
    # return True on success and False on errors
    return pisaStatus.err
