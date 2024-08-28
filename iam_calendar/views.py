from rest_framework.generics import CreateAPIView, ListAPIView
from datetime import datetime, UTC

from iam_calendar.models import Event
from iam_calendar.serializers import AddEventSerializer, ListEventSerializer
from iam_calendar.services import DateTimeServices


class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = AddEventSerializer


class EventListAPIView(ListAPIView):
    serializer_class = ListEventSerializer

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if DateTimeServices.is_valid_date(year, month, day):
            queryset = Event.objects.filter(date=datetime(year, month, day))
        return queryset
