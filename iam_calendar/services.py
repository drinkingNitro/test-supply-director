from datetime import datetime, timedelta, timezone

from iam_calendar.models import Event, EventTemplate


class DateTimeServices:
    @staticmethod
    def is_valid_date(year, month, day):
        try:
            date = datetime(year, month, day)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_timestamp_frome_date_and_time(date, time):
        dt = datetime.combine(date, time)
        dt_utc = dt.replace(tzinfo=timezone.utc)
        timestamp = int(dt_utc.timestamp())
        return timestamp

    @staticmethod
    def get_date_and_time_from_timestamp(timestamp):
        date_time = datetime.fromtimestamp(timestamp)
        date = date_time.date()
        time = date_time.time()
        return date, time

    @staticmethod
    def get_relative_timestamp_from_days(day_count):
        return day_count * 86400


class EventServices:
    @staticmethod
    def extend_chain(event_template, end_date):
        '''The method finds the latest event in the chain and adds subsequent events
        based on the period attribute until the end_date is reached.'''

        if not isinstance(event_template, EventTemplate):
            raise TypeError('Event must be an EventTemplate instance')

        latest_event_in_chain = event_template.events.latest('start_at')
        daily_time_of_event = latest_event_in_chain.time

        date_time_period = timedelta(days=event_template.period)
        next_chain_link_date = latest_event_in_chain.date + date_time_period
        events_to_extend = list()

        while next_chain_link_date <= end_date:
            unix_timestamp = DateTimeServices.get_timestamp_frome_date_and_time(
                date=next_chain_link_date, time=daily_time_of_event
            )
            next_event = Event(
                template=event_template,
                start_at=unix_timestamp,
                date=next_chain_link_date,
                time=daily_time_of_event
            )
            events_to_extend.append(next_event)
            next_chain_link_date += date_time_period

        Event.objects.bulk_create(events_to_extend)
