# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models


class Consumer(models.Model):
    """ Represents a single consumer. """
    AREAS = (
        (1, "Area 1"),
        (2, "Area 2")
    )
    TARIFFS = (
        (1, "Tariff 1"),
        (2, "Tariff 2"),
        (3, "Tariff 3")
    )

    user_id = models.IntegerField(primary_key=True)
    area = models.IntegerField(choices=AREAS)
    tariff = models.IntegerField(choices=TARIFFS)

    def __str__(self):
        return "(%d,%s,%s)" % (self.user_id, self.get_area_display(), self.get_tariff_display())

    def getConsumptions(self):
        return Consumption.objects.filter(consumer=self.user_id)

    def averageMagnitude(self):
        consumptions = self.getConsumptions()
        total = 0
        for consumption in consumptions:
            total += consumption.magnitude
        return total / len(consumptions)

    def averageMagnitudeForTimeOfDay(self, time):
        """ Gives you the average consumption magnitude attributed to this consumer at a given
        time of day for the last week. If there are no consumptions attributed at this time of day,
        then the returned result is None, not 0. """
        date = timezone.now()
        week = datetime.timedelta(days=600)
        consumptions =  Consumption.objects.filter(
            consumer=self.user_id, date_time__time=time, date_time__gte=date - week
        )
        if (len(consumptions) == 0):
            return None
        total = 0
        for consumption in consumptions:
            total += consumption.magnitude
        return total / len(consumptions)

    def areaAverageMagnitudeForTimesOfDay(area):
        """ Returns a list of dictionary objects consisting of {"time","value"}, where time is
        a given time of the day, and value is the average power used at this time in the given area.
        The times in the list are all times which have data attributed to them in this area. """
        date = timezone.now()
        week = datetime.timedelta(days=600)
        consumers = Consumer.objects.filter(area=area)
        consumptions = Consumption.objects.filter(consumer__area=area, date_time__gte=date - week)
        totals = {}

        # Get a list of all times that appear.
        for consumption in consumptions:
            isoTime = consumption.date_time.time().isoformat()
            if (isoTime not in totals):
                totals[isoTime] = [0, 0]

        # Get the use for each consumer in each time.
        for consumer in consumers:
            for total in totals:

                consumerMagnitude = consumer.averageMagnitudeForTimeOfDay(total)
                if (consumerMagnitude != None):
                    totals[total][0] += consumerMagnitude
                    totals[total][1] += 1

        # Average these totals.
        for total in totals:
            totals[total] = totals[total][0] / totals[total][1]

        return totals



class Consumption(models.Model):
    """ Represents a single piece of consumption information. Has a many to one relationship to
    Consumer, as a single consumer will have many pieces of consumption information related to
    them. """
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    date_time = models.DateTimeField("Date and time of consumption.")
    # No provided data actually makes use of decimal points, but considering that they are provided
    # with them suggests this could change without notice, so it is safest to store the data as
    # a float.
    magnitude = models.FloatField("Amount of energy consumed.")

    def __str__(self):
        return "(%d,%s,%1.1f)" % (self.consumer.user_id, self.date_time, self.magnitude)
