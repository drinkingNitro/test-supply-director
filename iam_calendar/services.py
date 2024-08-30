from datetime import datetime, UTC, date, time

class DateTimeServices:
    def is_valid_date(year, month, day):
        try:
            date = datetime(year, month, day)
            return True
        except ValueError:
            return False

    def timestamp_to_datefield(timestamp):
        dt = datetime.fromtimestamp(timestamp, UTC)
        return dt.date()

    def timestamp_to_timefield(timestamp):
        dt = datetime.fromtimestamp(timestamp, UTC)
        return dt.time()


class EventServices:
    ...