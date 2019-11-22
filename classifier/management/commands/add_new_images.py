from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from classifier.models import Image


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        if file_path is None:
            raise ValidationError('no data file argument provided')

        if file_path.split('.')[-1] != 'csv':
            raise ValidationError('not a csv file')

        with open(file_path, 'r') as f:
            urls = f.read().split(',\n')

        clear_urls = [u.replace('"', '').replace(',', '') for u in urls]

        no_created = 0
        no_fetched = 0

        print('adding %s to the database' % len(clear_urls))

        for url in clear_urls:
            image, created = Image.objects.get_or_create(url=url)
            if created:
                no_created += 1
            else:
                no_fetched += 1

        print('%s images already exist in the database' % no_fetched)
        print('%s new images added to the database' % no_created)
