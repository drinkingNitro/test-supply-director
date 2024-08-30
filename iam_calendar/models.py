from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    '''The model represents an Event in the calendar. If the period attribute is provided, it will be a chain event.
    The chain_id is an identifier of the chain and can be used to perform operations on the entire chain.
    This field is nullable to allow detaching an event from the chain and making it independent.'''

    name = models.CharField(_('Name'), max_length=50)
    start_at = models.PositiveIntegerField(_('Start at (Unix)'))
    date = models.DateField(_('Start date'), null=True, blank=True)
    time = models.TimeField(_('Start time'), null=True, blank=True)
    period = models.PositiveSmallIntegerField(_('Period (days)'), null=True, blank=True)
    chain_id = models.UUIDField(_('Chain ID'), default=None, null=True, blank=True, db_index=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
