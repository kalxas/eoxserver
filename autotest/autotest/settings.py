# -------------------------------------------------------------------------------
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Stephan Krause <stephan.krause@eox.at>
#          Stephan Meissl <stephan.meissl@eox.at>
#
# -------------------------------------------------------------------------------
# Copyright (C) 2011 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -------------------------------------------------------------------------------

"""
Django settings for EOxServer's autotest instance.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from os.path import join, abspath, dirname
from eoxserver.services.ows.wps.config import DEFAULT_EOXS_PROCESSES

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tmp'

PROJECT_DIR = dirname(abspath(__file__))
PROJECT_URL_PREFIX = ''

DEBUG = True

ADMINS = (
    # ('EOX', 'office@eox.at'),
)

MANAGERS = ADMINS

# Configure which database to use. Default is spatialite.
db_type = os.environ.get('DB', 'postgis')
if db_type == 'postgis':
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': os.environ['DB_HOST'],
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PW'],
        }
    }
elif db_type == 'spatialite':
    spatialite_path = os.environ.get('SPATIALITE_PATH', 'data/config.sqlite')
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': join(PROJECT_DIR, spatialite_path),
        }
    }

    SPATIALITE_SQL = join(PROJECT_DIR, 'data/init_spatialite-2.3.sql')
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite.so'

# Use faster ramfs tablespace for testing in case of PostGIS e.g. in Jenkins
# Configure via:
#    mount -t ramfs none /mnt/
#    mkdir /mnt/pgdata/
#    chown postgres:postgres /mnt/pgdata/
#    su postgres
#    psql -d postgres -c "CREATE TABLESPACE ramfs LOCATION '/mnt/pgdata'"
#    psql -d postgres -c "GRANT CREATE ON TABLESPACE ramfs TO jenkins;"
#    exit
#from sys import argv
#if 'test' in argv:
#    DEFAULT_TABLESPACE = 'ramfs'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# Note that this is the time zone to which Django will convert all
# dates/times -- not necessarily the timezone of the server.
# If you are using UTC (Zulu) time zone for your data (e.g. most
# satellite imagery) it is highly recommended to use 'UTC' here. Otherwise
# you will encounter time-shifts between your data, search request & the
# returned results.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # # For management of the per/request cache system.
    # 'eoxserver.backends.middleware.BackendsCacheMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # # For management of the per/request cache system.
    # 'eoxserver.backends.middleware.BackendsCacheMiddleware',
)

ROOT_URLCONF = 'autotest.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'autotest.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # Enable the databrowse:
    #'django.contrib.databrowse',
    # Enable for better schema and data-migrations
    # Enable for debugging
    # 'django_extensions',
    'django_prometheus',
    # Enable EOxServer:
    'eoxserver.core',
    'eoxserver.services',
    'eoxserver.resources.coverages',
    'eoxserver.backends',
    'eoxserver.testing',
    'eoxserver.webclient',
    # Enable EOxServer autotests
    'autotest_services',
    'autotest_coverages',
)


# The configured EOxServer components. Components add specific functionality
# to the EOxServer and must adhere to a given interface. In order to activate
# a component, its module must be included in the following list or imported at
# some other place. To help configuring all required components, each module
# path can end with either a '*' or '**'. The single '*' means that all direct
# modules in the package will be included. With the double '**' a recursive
# search will be done.
COMPONENTS = ()

EOXS_PROCESSES = DEFAULT_EOXS_PROCESSES + [
    'autotest_services.processes.test00_identity_literal.TestProcess00',
    'autotest_services.processes.test01_identity_bbox.TestProcess01',
    'autotest_services.processes.test02_identity_complex.TestProcess02',
    'autotest_services.processes.test03_binary_complex.TestProcess03',
    'autotest_services.processes.test04_datetime_tzaware_input.TestProcess04',
    'autotest_services.processes.test05_datetime_tzaware_output.TestProcess05',
    'autotest_services.processes.test06_minimal_process.Test06MinimalValidProcess',
    'autotest_services.processes.test06_minimal_process.Test06MinimalAllowedProcess',
    'autotest_services.processes.test07_request_parameter.Test07RequestParameterTest',
    'autotest_services.processes.test08_get_statistics.Test08GetStatistics',
    'autotest_services.processes.test09_get_statistics_complex.Test09GetStatisticsComplex',
]


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s][%(module)s] %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'eoxserver_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_DIR, 'logs', 'eoxserver.log'),
            'formatter': 'verbose' if DEBUG else 'simple',
            'filters': [],
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(PROJECT_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
            'filters': [],
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': [],
        }
    },
    'loggers': {
        'eoxserver': {
            'handlers': ['eoxserver_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False
        },
        'django': {
            'handlers': ['django_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    }
}

FIXTURE_DIRS = (
    join(PROJECT_DIR, 'data/fixtures'),
)

# Set this variable if the path to the instance cannot be resolved
# automatically, e.g. in case of redirects
#FORCE_SCRIPT_NAME="/path/to/instance/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
