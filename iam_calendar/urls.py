from django.urls import path
from iam_calendar.views import EventCreateAPIView, EventListAPIView

app_name = 'calendar'

urlpatterns = [
    path('add/', EventCreateAPIView.as_view(), name='event-create'),
    path('events/<int:year>/<int:month>/<int:day>/', EventListAPIView.as_view(), name='event-list'),
]

