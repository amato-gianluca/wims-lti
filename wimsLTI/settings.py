# -*- coding: utf-8 -*-
#
#  settings.py
#
#  Authors:
#       - Coumes Quentin <coumes.quentin@gmail.com>
#


"""
Django settings for wimsLTI project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

from apscheduler.triggers.cron import CronTrigger
from django.contrib.messages import constants as messages

from lti_app.enums import Role


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-qj!o^8$@!&7))^77^z8(-5rp*5x=7q(736)05x$h(inkfm^1#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Set to true when 'python3 manage.py test' is used
TESTING = sys.argv[1:2] == ['test']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'lti_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wimsLTI.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS':  {
            'debug':              DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wimsLTI.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Logging informations
LOGGING = {
    'version':                  1,
    'disable_existing_loggers': False,
    'filters':                  {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true':  {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters':               {
        'simple': {
            'format':  ("[%(asctime)-15s] [%(pathname)s]"
                        "[%(filename)s:%(funcName)s:%(lineno)d]"
                        " %(levelname)s -- %(message)s"),
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },
    'handlers':                 {
        'console':     {
            'level':     'DEBUG',
            'filters':   ['require_debug_true'],
            'class':     'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level':        'WARNING',
            'class':        'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter':    'simple'
        }
    },
    'loggers':                  {
        '':               {
            'handlers': ['console', 'mail_admins'],
            'level':    'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level':    'ERROR',
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Define parameters which must be present in the LTI request
LTI_MANDATORY = [
    'lti_message_type',
    'lti_version',
    'resource_link_id',
    'oauth_consumer_key',
    'oauth_signature_method',
    'oauth_timestamp',
    'oauth_nonce',
    'oauth_signature',
]
WIMSLTI_MANDATORY = [
    'context_id',
    'context_title',
    'user_id',
    'tool_consumer_instance_guid',
    'tool_consumer_instance_description',
    'launch_presentation_locale',
    'lis_person_contact_email_primary',
    'lis_person_name_family',
    'lis_person_name_given',
    'roles',
]

MESSAGE_TAGS = {
    messages.DEBUG:   'alert-info',
    messages.INFO:    'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR:   'alert-danger',
}

# List of Roles that are allowed to create new classes on the WIMS servers
# Any user connecting from an LMS with one of these role will also be logged
# in as the class' supervisor on the WIMS server
ROLES_ALLOWED_CREATE_WIMS_CLASS = [
    Role.ADMINISTRATOR,
    Role.INSTRUCTOR,
    Role.STAFF,
]

# Static files
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

# Directory containing mail's title and body
MAIL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mail")

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# XML used to sent grade back to the LMS
with open(os.path.join(BASE_DIR, "lti_app/ressources/replace.xml"), encoding="utf-8") as f:
    XML_REPLACE = f.read()

# The CronTrigger triggering the job sending every grade of the WIMS server to the LMS, see
# https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html for more information.
SEND_GRADE_BACK_CRON_TRIGGER = CronTrigger(
    year="*",
    month="*",
    day="*",
    week="*",
    day_of_week="*",
    hour="7, 19",
    minute="0",
    second="0",
)

# The CronTrigger triggering the job checking that for every class registered on wims-lti, the
# corresponding class exists on its WIMS server, deleting the instance on wims-lti if not, see
# # https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html for more information.
CHECK_CLASSES_EXISTS_CRON_TRIGGER = CronTrigger(
    year="*",
    month="*",
    day="*",
    week="*",
    day_of_week="*",
    hour="7, 19",
    minute="0",
    second="0",
)

# Time before requests sent to a WIMS server from wims-lti time out. Should be increased
# if some WIMS server contains a lot of classes / users.
WIMSAPI_TIMEOUT = 5

# Allow the file 'wimsLTI/config.py' to override these settings.
from wimsLTI.config import *  # noqa: E402 F401 F403
