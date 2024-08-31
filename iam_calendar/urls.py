from django.urls import path

from iam_calendar.views import (CreateEventAPIView, DeleteEventView,
                                ForwardDeleteEventView, ListEventsAPIView,
                                UpdateEventAPIView)

app_name = 'calendar'

urlpatterns = [
    path('add/', CreateEventAPIView.as_view(), name='event-create'),
    path('events/<int:year>/<int:month>/<int:day>/', ListEventsAPIView.as_view(), name='event-list'),
    path('update/<int:id>/<int:year>/<int:month>/<int:day>/', UpdateEventAPIView.as_view(), name='event-update'),
    path('remove/<int:id>/<int:year>/<int:month>/<int:day>/', DeleteEventView.as_view(), name='event-delete'),
    path('remove-next/<int:id>/<int:year>/<int:month>/<int:day>/', ForwardDeleteEventView.as_view(), name='event-delete-next'),
]

