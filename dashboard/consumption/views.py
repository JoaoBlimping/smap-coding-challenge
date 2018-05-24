# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from consumption.models import Consumer, Consumption

# Create your views here.


def summary(request):
    context = {
        "users": Consumer.objects.filter(area=1),
        "first": json.dumps(Consumer.areaAverageMagnitudeForTimesOfDay(1))
    }
    return render(request, 'consumption/summary.html', context)


def detail(request):
    context = {
    }
    return render(request, 'consumption/detail.html', context)
