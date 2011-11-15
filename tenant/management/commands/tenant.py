from django.core.management.base import BaseCommand, CommandError

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, subcommand, **kwargs):
        pass

    def create(self):
        pass

    def delete(self):
        pass

    def info(self):
        pass
