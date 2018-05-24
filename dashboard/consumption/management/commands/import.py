import time
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.core.management.base import BaseCommand
from consumption.models import Consumer, Consumption

def parseCsv(lines):
    """ Parses a CSV file, and returns a list of dictionaries of all values, unless the file was
    deformed, in which case it throws AN ERROR. """
    params = lines[0][:-1].split(",")
    output = []

    for line in lines[1:]:
        values = line[:-1].split(",")
        if (len(values) != len(params)):
            raise ValueError("Line '%s' has the wrong number of values." % line)
        else:
            item = {}
            for i,param in enumerate(params):
                item[param] = values[i]
            output.append(item)
    return output





class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("skip", nargs="?", type=int, default=1)


    def handle(self, *args, **options):
        # Optional argument.
        if (options["skip"]): skip = options["skip"]
        else: skip = 1

        # Load in consumers.
        userFile = open("../data/user_data.csv", "r")
        consumersData = parseCsv(userFile.readlines())
        userFile.close()
        consumptionsData = []

        # Iterate through consumers and load in the data pertaining to them.
        for consumerData in consumersData:
            consumptionFile = open("../data/consumption/%s.csv" % consumerData["id"], "r")
            consumptionsData.append(parseCsv(consumptionFile.readlines()))
            consumptionFile.close()

        # Iterate through consumers again and save them and the data relating to them
        for i,consumerData in enumerate(consumersData):
            area = int(consumerData["area"][1])
            tariff = int(consumerData["tariff"][1])
            consumer = Consumer(
                user_id=consumerData["id"], area=area, tariff=tariff
            )
            consumer.save()
            print("Consumer %d out of %d" % (i,len(consumersData)))

            for u,consumptionData in enumerate(consumptionsData[i]):
                if (u % skip != 0): continue

                dateTime = make_aware(parse_datetime(consumptionData["datetime"]))
                magnitude = float(consumptionData["consumption"])

                consumption = Consumption(
                    consumer=consumer,
                    date_time=dateTime,
                    magnitude=magnitude
                )
                consumption.save()
