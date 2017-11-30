class Room:
    def __init__(self, _id, office, start_date, end_date, host, room='Room A'):
        self.id = _id
        self.office = office
        self.start_date = start_date
        self.end_date = end_date
        self.host = host if host else 'EMPTY HOST'
        self.seconds = (self.end_date - self.start_date).seconds
        self.hours = self.seconds // 3600
        self.delta = self.end_date - self.start_date
        self.room = room

    def convert_hours_to_str(self):
        return '%s:%s hr' % (self.convert_hours(self.delta[0]), self.get_seconds(self.delta[1]))

    def convert_hours(self):
        return '0' + str(self.hours) if len(str(self.hours)) == 1 else str(self.hours)

    def get_seconds(self):
        res = (self.seconds // 60) % 60
        return str(res) if res else '00'


class RoomOffice:
    _50 = '50'
    _51 = '51'

    ROOMS = {
        _50: 'Room A',
        _51: 'Room B'
    }

    @staticmethod
    def get_name_room(room):
        return RoomOffice.ROOMS[room]
