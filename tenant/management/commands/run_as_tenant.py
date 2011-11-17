from django.core.management.base import BaseCommand, CommandError
from django.core.management import get_commands, call_command, load_command_class

from optparse import make_option, OptionParser
import sys

from tenant import authenticate


class Command(BaseCommand):
    option_list = (
        make_option('--tenant', default=None),
    )
        
    def run_from_argv(self, argv):
        argv.pop(1)
        self.subcommand = argv[1]
        return super(Command, self).run_from_argv(argv)

    def create_parser(self, prog_name, subcommand):
        name = subcommand
        try:
            app_name = get_commands()[name]
            if isinstance(app_name, BaseCommand):
                # If the command is already loaded, use it directly.
                klass = app_name
            else:
                klass = load_command_class(app_name, name)
        except KeyError:
            raise CommandError("Unknown command: %r" % name)
        
        self.option_list += klass.option_list
        parser = super(Command, self).create_parser(prog_name, subcommand)
        return parser

    def handle(self, *args, **kwargs):
#        print args, kwargs
        tenant = kwargs.pop('tenant', None)
        if tenant:
            print authenticate(name=tenant)
        call_command(self.subcommand, *args, **kwargs)
