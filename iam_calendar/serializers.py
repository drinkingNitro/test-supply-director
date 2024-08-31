from rest_framework import serializers

from iam_calendar.models import Event, EventTemplate
from iam_calendar.services import DateTimeServices


class ReturnEventSerializer(serializers.ModelSerializer):
    '''Serializes response for create event view.'''

    class Meta:
        model = Event
        fields = ['id',]


class CreateEventSerializer(serializers.ModelSerializer):
    '''Deserializes request for create event view.'''
    
    name = serializers.CharField(max_length=50)
    period = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'period', 'start_at',]

    def create(self, validated_data):
        '''Creates event template and then creates event itself.'''

        name = validated_data.pop('name')
        period = None
        try:
            period = validated_data.pop('period')
        except KeyError:
            pass

        template = EventTemplate.objects.create(name=name, period=period)

        start_at_unix = validated_data['start_at']
        date, time = DateTimeServices.get_date_and_time_from_timestamp(start_at_unix)

        event = Event.objects.create(
            template=template,
            start_at=start_at_unix,
            date=date,
            time=time
        )

        return event


class EventsListSerializer(serializers.ModelSerializer):
    '''Serializes response for get (list) event view.'''

    name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.template.name


class EventUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Event
        fields = ['id', 'name']
        read_only_fields = ['id',]

    def update(self, instance, validated_data):
        '''Since the name is an attribute of EventTemplate, it is necessary to detach the updating event 
        from the existing chain and attach it to a different (individual) template.'''

        if instance.template.period:
            new_template = EventTemplate.objects.create(name=validated_data.get('name'), period=None)
            instance.template = new_template
        else:
            instance.template.name = validated_data.get('name')
            instance.template.save()
        instance.save()

        return instance
