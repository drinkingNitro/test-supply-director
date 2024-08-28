from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import timedelta


class Event(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    start_at = models.PositiveIntegerField(_('Start at (Unix)'))
    date = models.DateField(_('Start date'), null=True, blank=True)
    time = models.TimeField(_('Start time'), null=True, blank=True)
    period = models.PositiveSmallIntegerField(_('Period (days)'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
