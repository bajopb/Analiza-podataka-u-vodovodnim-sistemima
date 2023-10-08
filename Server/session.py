from datetime import datetime

class Session:
    def __init__(self, session_id, src, dst):
        self.id = session_id
        self.src = src
        self.dst = dst
        self.start_time = None
        self.end_time = None
        self.duration = None

    def start_session(self, start_time):
        self.start_time = start_time

    def end_session(self, end_time):
        self.end_time = end_time

    def calculate_duration(self):
        if self.start_time is None or self.end_time is None:
            raise ValueError("Start time and end time must be set to calculate duration.")
        start_datetime = datetime.strptime(self.start_time, '%H:%M:%S')
        end_datetime = datetime.strptime(self.end_time, '%H:%M:%S')
        duration = end_datetime - start_datetime
        return duration.total_seconds()