from rest_framework.serializers import ModelSerializer

from iam_calendar.models import Event
from iam_calendar.services import DateTimeServices


class AddEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start_at', 'period',)
        extra_kwargs = {
            'name': {'write_only': True},
            'start_at': {'write_only': True},
            'period': {'write_only': True},
        }

    def create(self, validated_data):
        '''Extracts start_at from validated_data, converts it to date and time,
        adds them to the instance as separate fields, and then saves the instance.'''

        start_at = validated_data.get('start_at')
        date = DateTimeServices.timestamp_to_datefield(start_at)
        time = DateTimeServices.timestamp_to_timefield(start_at)
        event = Event.objects.create(date=date, time=time, **validated_data)
        return event


class ListEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name',)
