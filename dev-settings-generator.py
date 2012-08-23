#!/usr/bin/python2.7
"""
Generates dev_settings.py for Django.

Generates 3 files:
* dev_settings.py
* dev_settings_generated.py
* dev_settings_custom.py

dev_settings.py and dev_settings_generated.py should not be modified by hand.
You can modify dev_settings_custom.py to create custom settings.  
"""

import argparse
from distutils.sysconfig import get_python_lib
from os import path
import sys

class Command(object):
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('project', type=str, nargs=1)
        parser.add_argument('--debug-toolbar', action='store_true', help='add django debug toolbar to generated settings')
        parser.add_argument('--include', action='append', help='include file from ~/.dev-settings-generator/include/*.py')
        parser.add_argument('--postgis', action='store_true', help='use postgis django db backend')
        parser.add_argument('--sqlite', action='store_true', help='use sqlite3 django db backend')
        self.generate_settings_file(parser.parse_args())
        self.create_custom_settings_file()

        self.create_main_settings_file()

    def create_custom_settings_file(self):
        open('dev_settings_custom.py', 'w+').close()

    def create_main_settings_file(self):
        with open('dev_settings.py', 'w+') as settings:
            settings.write("#!/usr/bin/python\n")
            settings.write(self.generator_information())
            settings.write(
                "from dev_settings_generated import *\n"
                "from dev_settings_custom import *\n"
            )

    def generate_settings_file(self, args):
        project = args.project[0].replace('_', '-')
        with open('dev_settings_generated.py', 'w') as settings:
            settings.write("#!/usr/bin/python\n")
            settings.write(self.generator_information())
            settings.write(self.import_project_settings(project))
            settings.write("DEBUG = True\nTEMPLATE_DEBUG = True \n")
            settings.write(self.database_settings(project, postgis=args.postgis, sqlite=args.sqlite))
            if(args.debug_toolbar):
                settings.write(self.debug_toolbar())
            settings.write(self.include_files(args.include))

    def import_project_settings(self, project):
        return "from %s.settings import *\n" % project.replace('-', '_')

    def database_settings(self, project, postgis=False, sqlite=False):
        database_backend = 'django.db.backends.postgresql_psycopg2'
        database_name = project
        if postgis:
            database_backend = 'django.contrib.gis.db.backends.postgis'
        elif sqlite:
            database_backend = 'django.db.backends.sqlite3'
            site_packages = get_python_lib()
            database = '%s.sqlite' % project
            database_name = path.join(site_packages, database)

        return (
            "DATABASES = {\n"
            "    'default': {\n"
            "        'ENGINE': '%s',\n"
            "        'NAME': '%s',\n"
            "    }\n"
            "}\n"
        ) % (database_backend, database_name)

    def debug_toolbar(self):
        return (
            "INSTALLED_APPS += ('debug_toolbar',)\n"
            "INTERNAL_IPS = ('127.0.0.1',)\n"
            "DEBUG_TOOLBAR_CONFIG = {\n"
            "    'INTERCEPT_REDIRECTS': False,\n"
            "}\n"
            "MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)\n"
        )

    def generator_information(self):
        return (
            "# Generated automatically with parameters:\n"
            "# " + " ".join(sys.argv[1:]) + "\n"
        )

    def include_files(self, files):
        result = ""
        for filename in files or []:
            filepath = path.expanduser('~/.dev-settings-generator/include/%s.py' % filename)
            result += "\n\n# %s\n" % filepath
            result += open(filepath).read()
        return result

if __name__ == '__main__':
    Command().run()
