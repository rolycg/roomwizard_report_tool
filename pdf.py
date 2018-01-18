from xhtml2pdf import pisa

beginHtml = "<html> <style> @page {size: letter portrait;@frame content_frame {left: 50pt;top: 50pt;right: 50pt; }}" \
            ".left{margin-left: 0cm;margin-right: 0cm;} " \
            ".header-resume { align:left; width:40%;}" \
            "</style><body>"
endHtml = "</body></html>"
outputFilename = " usage.pdf"


def generate_row(row):
    res = "<tr>"
    res += '<td align="left">' + row.room + '</td>'
    res += '<td align="left">' + str(row.start_date.strftime("%m/%d/%y %H:%M:%S")) + '</td>'
    res += '<td align="left">' + str(row.end_date.strftime("%m/%d/%y %H:%M:%S")) + '</td>'
    res += '<td align="left">' + convert_standard_hour(row.seconds) + '</td>'
    res += '<td align="left">' + row.host + '</td>'
    res += "</tr>"
    return res


def convert_standard_hour(seconds):
    return convert_hours_to_str_2((int(seconds) // 3600, (int(seconds) // 60) % 60))

def generate_data(rooms):
    general = {}
    details = {}
    for key in rooms.keys():
        room = rooms[key]
        try:
            details[room.host].append(generate_row(room))
        except:
            details[room.host] = [generate_row(room)]
        try:
            general[room.host] += room.seconds
        except:
            general[room.host] = room.seconds
    return details, general


def generate_row_session(data):
    final = {}
    for key in data.keys():
        room = data[key]
        try:
            times = final[room.host]
            try:
                times[str(room.seconds)] += 1
            except:
                times[str(room.seconds)] = 1
        except:
            final[room.host] = {
                str(room.seconds): 1
            }
    res = ''
    for host in final.keys():

        for session in sorted(final[host].keys(), key=lambda x: int(x), reverse=True):
            tmp = "<tr>"
            tmp += '<td align="left">' + host + '</td>'
            tmp += '<td align="left">' + convert_hours_to_str_2(
                (int(session) // 3600, (int(session) // 60) % 60)) + '</td>'
            tmp += '<td align="left">' + quantity(str(final[host][session])) + '</td>'
            res += tmp + "</tr>"
    return res


def quantity(number):
    return ('0' * len(number)) + number if len(number) == 1 else number


def get_hours(elapsed):
    return (elapsed.days * 24) + (elapsed.seconds // 3600), elapsed


def get_seconds(elapsed):
    res = (elapsed.seconds // 60) % 60
    return str(res) if res else '00'


def convert_hours(elapsed):
    return '0' + str(elapsed) if len(str(elapsed)) == 1 else str(elapsed)


def convert_hours_to_str_2(time):
    return '%s:%s hr' % (convert_hours(time[0]), str(time[1]) if time[1] else '00')


def convert_hours_to_str(elapsed):
    return '%s:%s hr' % (convert_hours(elapsed[0]), get_seconds(elapsed[1]))


def generate_resume_row(data):
    res_list = []
    res = ''
    for x in data.keys():
        for y in data[x].keys():
            res_list.append((str(x), get_hours(data[x][y]), str(y)))

    res_list.sort(key=lambda x: (-x[1][0], -x[1][1]))

    for x in res_list:
        res += '<tr>'
        res += '<td align="left">' + str(x[0]) + '</td>'
        res += '<td align="left">' + str(convert_hours_to_str(x[1])) + '</td>'
        res += '<td align="left">' + str(x[2]) + '</td>'
        res += "</tr>"
    return res


def generate_header(fields):
    res = "<tr>"
    for field in fields:
        res += '<th align="left">' + field + '</th>'
    res += "</tr>"
    return res


def header_resume_host(fields):
    res = "<tr>"
    res += '<th align="left" width="40%">' + fields[0] + '</th>'
    res += '<th align="left" width="30%">' + fields[1] + '</th>'
    res += '<th align="left" width="30%">' + fields[2] + '</th>'
    return res


def convert_resume_data(rooms):
    data = {}
    for key in rooms.keys():
        room = rooms[key]
        office_hour = data.get(room.host)
        if office_hour:
            hour = office_hour.get(room.office)
            if hour:
                office_hour[room.office] += room.delta
            else:
                office_hour[room.office] = room.delta
        else:
            data[room.host] = {room.office: room.delta}
    return data


def convertHtmlToPdf(room, start_date, end_date, letter):
    # rows = ""
    # for row in room.keys():
    #     rows += generate_row(room[row])

    details, general = generate_data(room)

    main_header = '<div align="center"><h1> 34 / EAST / 51 / STREET </h1> <h3>7th Floor Conference Room Usage</h3> </div>'

    header = generate_header(('OFFICE', 'START DATE', 'END DATE', 'SESSION', 'HOST'))
    div = '<div align="center" class="left" > <h2 align="center">' + '<h3>' + start_date + ' - ' + end_date + '</h3>' + '</h2>'

    table = ''
    for keys in details.iterkeys():
        rows = ''.join(details[keys])
        table += '<div align="center" class="left"> <h2 align="center">' + '<h3>' + str(keys) + ': ' + convert_standard_hour(
            general[keys]) + ' total usage </h3>' + '</h2>'
        table += '<table>' + header + rows + '</table></div>'
        table += '<br/>'

    # header_resume = header_resume_host(('HOST', 'HOURS', 'OFFICE'))
    # rows_resume = generate_resume_row(convert_resume_data(room))
    # resume = '<div align="center" class="left" > <h2 align="center">By Host</h2><table>' + header_resume + rows_resume + '</table></div>'
    # jump = '<p style="page-break-after: always;">&nbsp;</p>'
    # _break = '<br/>'
    #
    # header_session = header_resume_host(('HOST', 'SESSION', 'TIMES'))
    # rows_session = generate_row_session(room)
    # session = '<div align="center" class="left" > <h2 align="center">By Session</h2><table>' + header_session + rows_session + '</table></div>'

    html_parts = [
        beginHtml,
        main_header,
        # resume,
        # _break,
        # session,
        # jump,
        div,
        table,
        endHtml
    ]

    source_html = ''.join(html_parts)
    result_file = open(letter + outputFilename, "w+b")

    pisaStatus = pisa.CreatePDF(
        source_html,  # the HTML to convert
        dest=result_file)  # file handle to recieve result
    # close output file
    result_file.close()  # close output file
    # return True on success and False on errors
    return pisaStatus.err
