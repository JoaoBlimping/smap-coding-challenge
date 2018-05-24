# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Consumer, Consumption


class ConsumerModelTests(TestCase):
    time = timezone.now()

    def setUp(self):
        halfHour = datetime.timedelta(minutes=30)
        hour = datetime.timedelta(minutes=60)
        day = datetime.timedelta(days=1)

        a = Consumer.objects.create(user_id=3000, area=2, tariff=3)
        b = Consumer.objects.create(user_id=3001, area=1, tariff=1)

        Consumption.objects.create(consumer=a, date_time=self.time, magnitude=1.0)
        Consumption.objects.create(consumer=a, date_time=self.time - halfHour, magnitude=2.0)
        Consumption.objects.create(consumer=a, date_time=self.time - hour, magnitude=3.0)
        Consumption.objects.create(consumer=a, date_time=self.time + day, magnitude=4.0)
        Consumption.objects.create(consumer=b, date_time=self.time, magnitude=4.0)
        Consumption.objects.create(consumer=b, date_time=self.time - halfHour, magnitude=5.0)
        Consumption.objects.create(consumer=b, date_time=self.time - hour, magnitude=6.0)
        Consumption.objects.create(consumer=b, date_time=self.time + day, magnitude=7.0)

    def test_toString(self):
        """ Make sure it is converting itself to a string correctly. """
        c = Consumer.objects.get(user_id=3000)
        self.assertEqual(c.__str__(), "(3000,Area 2,Tariff 3)")

    def test_consumptions(self):
        """ Make sure it is getting the consumptions that belong to it correctly. """
        consumptions = Consumer.objects.get(user_id=3000).getConsumptions()
        self.assertIs(Consumption.objects.get(pk=1) in consumptions, True)
        self.assertIs(Consumption.objects.get(pk=2) in consumptions, True)
        self.assertIs(Consumption.objects.get(pk=3) in consumptions, True)
        self.assertIs(Consumption.objects.get(pk=4) in consumptions, True)
        self.assertIs(Consumption.objects.get(pk=5) in consumptions, False)
        self.assertIs(Consumption.objects.get(pk=6) in consumptions, False)
        self.assertIs(Consumption.objects.get(pk=7) in consumptions, False)
        self.assertIs(Consumption.objects.get(pk=8) in consumptions, False)

    def test_averageMagnitude(self):
        """ Make sure the average magnitude is calculated correctly. """
        self.assertEqual(Consumer.objects.get(user_id=3000).averageMagnitude(), 2.5)
        self.assertEqual(Consumer.objects.get(user_id=3001).averageMagnitude(), 5.5)

    def test_averageMagnitudeForTimeOfDay(self):
        """ Make sure the average magnitude for a given time of day is calculated correctly """
        halfHour = datetime.timedelta(minutes=30)
        quaterHour = datetime.timedelta(minutes=15)
        self.assertEqual(
            Consumer.objects.get(user_id=3000).averageMagnitudeForTimeOfDay(self.time), 2.5
        )
        self.assertEqual(
            Consumer.objects.get(user_id=3000).averageMagnitudeForTimeOfDay(self.time - halfHour),
            2.0
        )
        self.assertEqual(
            Consumer.objects.get(user_id=3001).averageMagnitudeForTimeOfDay(self.time), 5.5
        )
        self.assertEqual(
            Consumer.objects.get(user_id=3000).averageMagnitudeForTimeOfDay(self.time - quaterHour),
            None
        )

    def test_areaAverageMagnitudeForTimesOfDay(self):
        halfHour = datetime.timedelta(minutes=30)
        hour = datetime.timedelta(hours=1)

        first = Consumer.areaAverageMagnitudeForTimesOfDay(1)
        self.assertIs(self.time.time().isoformat() in first, True)
        self.assertIs((self.time - halfHour).time().isoformat() in first, True)
        self.assertIs((self.time - hour).time().isoformat() in first, True)
        self.assertEqual(first[self.time.time().isoformat()], 5.5)


class ConsumptionModelTests(TestCase):
    def test_toString(self):
        """ Make sure it is converting itself to a string correctly. """
        time = timezone.now()
        consumer = Consumer(user_id=3975, area=2, tariff=3)
        c = Consumption(consumer=consumer, date_time=time, magnitude=1248.0)
        self.assertEqual(c.__str__(), "(3975,%s,1248.0)" % time)
