from django.core.management import BaseCommand
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Started gpio-worker")

        print("can do some work ;)")

        while True:
            print("next gpio update")

            time.sleep(6)

        # here place some loop that will get info fro m db (once per minute?) and do some gpio