from datetime import date, timedelta

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from iam_calendar.models import Event, EventTemplate
from iam_calendar.serializers import (CreateEventSerializer,
                                      EventsListSerializer,
                                      EventUpdateSerializer,
                                      ReturnEventSerializer)
from iam_calendar.services import DateTimeServices, EventServices


class CreateEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        '''When the period attribute is provided, creates an initial chain of events for 30 days.
        Otherwise creates just a single event.'''

        create_serializer = CreateEventSerializer(data=request.data)
        if create_serializer.is_valid():
            event = create_serializer.save()

            if event.template.period:
                forecast_date = event.date + timedelta(days=30)
                EventServices.extend_chain(event_template=event.template, end_date=forecast_date)


            response_serializer = ReturnEventSerializer(event)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListEventsAPIView(generics.ListAPIView):
    serializer_class = EventsListSerializer

    def get_queryset(self):
        '''If the requested combination of year, month, and day forms a valid date, 
        extends all existing periodic events until the requested date is reached. 
        Then filters the queryset by the requested date.'''

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if DateTimeServices.is_valid_date(year, month, day):
            requested_date = date(year, month, day)
        else:
            return Response({'error': 'Invalid date requested.'}, status=status.HTTP_400_BAD_REQUEST)

        periodic_events = EventTemplate.objects.filter(period__isnull=False).distinct()
        for event_template in periodic_events:
            EventServices.extend_chain(event_template=event_template, end_date=requested_date)
        queryset = Event.objects.filter(date=requested_date).select_related('template').order_by('time')
        return queryset


class UpdateEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if DateTimeServices.is_valid_date(year, month, day):
            requested_date = date(year, month, day)
        else:
            return Response({'error': 'Invalid date requested.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id, date=requested_date)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEventView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if DateTimeServices.is_valid_date(year, month, day):
            requested_date = date(year, month, day)
        else:
            return Response({'error': 'Invalid date requested.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id, date=requested_date)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ForwardDeleteEventView(APIView):
    def post(self, request, *args, **kwargs):
        '''Deletes all subsequent chain links as well as the requested event.'''

        event_id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if DateTimeServices.is_valid_date(year, month, day):
            requested_date = date(year, month, day)
        else:
            return Response({'error': 'Invalid date requested.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(id=event_id, date=requested_date)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        next_events_in_chain = Event.objects.filter(template=event.template, start_at__gt=event.start_at)
        next_events_in_chain.delete()
        return Response({'message': 'Event and subsequent event chain deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)
