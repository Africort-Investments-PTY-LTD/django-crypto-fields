import sys

from django.conf import settings
from django.core.management.color import color_style
from django.core.management.base import BaseCommand, CommandError

from ...keys import Keys


class Command(BaseCommand):
    help = 'Generate RSA asymmetric keys, AES symmetric keys and a salt.'

    def add_arguments(self, parser):
        # parser.add_argument('keypath', nargs=1, type=str)
        style = color_style
        try:
            default_path = settings.KEY_PATH
        except AttributeError:
            sys.stdout(style.INFO(
                f'setting.KEY_PATH not found. Using path=\'{settings.BASE_DIR}\''))
            default_path = settings.BASE_DIR
        try:
            default_prefix = settings.KEY_PREFIX
        except AttributeError:
            sys.stdout(style.INFO(
                f'setting.KEY_PREFIX not found. Using prefix=\'{settings.BASE_DIR}\''))
            default_prefix = 'user'

        parser.add_argument(
            '--keypath',
            action='store',
            dest='keypath',
            default=default_path,
            help=f'Set key path to something other than the \'{default_path}\'')
        parser.add_argument(
            '--keyprefix',
            action='store',
            dest='keyprefix',
            default=default_prefix,
            help=f'Set key prefix to something other than \'{default_prefix}\'')

    def handle(self, *args, **options):
        try:
            Keys.create_keys(
                prefix=options['keyprefix'], path=options['keypath'])
        except (FileNotFoundError, FileExistsError, OSError) as e:
            raise CommandError(e)
