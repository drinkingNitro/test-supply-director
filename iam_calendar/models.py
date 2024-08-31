from django.db import models
from django.utils.translation import gettext_lazy as _


class EventTemplate(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    period = models.PositiveSmallIntegerField(_('Period (days)'), null=True, blank=True)

    def __str__(self):
        return self.template.name

    class Meta:
        ordering = ('id',)
        db_table = 'event_templates'
        verbose_name = 'Event Template'
        verbose_name_plural = 'Event Templates'


class Event(models.Model):
    template = models.ForeignKey(to='EventTemplate', on_delete=models.CASCADE, related_name='events')
    start_at = models.PositiveIntegerField(_('Start at (Unix)'))
    date = models.DateField(_('Start date'), null=True, blank=True)
    time = models.TimeField(_('Start time'), null=True, blank=True)

    def __str__(self):
        return self.template.name

    class Meta:
        ordering = ('id',)
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
