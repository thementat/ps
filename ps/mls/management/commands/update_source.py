'''
Created on Apr 14, 2017

@author: chrisbradley
'''

from mls.models import Source
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('source_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for source_id in options['source_id']:
            try:
                source = Source.objects.get(pk=source_id)
            except Source.DoesNotExist:
                raise CommandError('Source "%s" does not exist' % source_id)
        source.update()