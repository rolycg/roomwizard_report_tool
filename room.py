

class Room:
    def __init__(self, office, start_date, end_date, host):
        self.office = office
        self.start_date = start_date
        self.end_date = end_date
        self.host = host if host else 'EMPTY'
