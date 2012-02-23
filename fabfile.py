from armstrong.dev.tasks import *
import tempfile

settings = {
    'DEBUG': True,
    'INSTALLED_APPS': (
        'django_hinting_cache',
    ),
    'ROOT_URLCONF': 'armstrong.apps.related_content.tests_related_content_support',
    'SITE_ID': 1,
    'STATIC_URL': '/static/',
    'CACHES': {
    	'default': {
    		'BACKEND': 'django_hinting_cache.cache.HintingCache',
    		'LOCATION': 'real',
    	},
	    'real': {
	        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
	        'LOCATION': 'unique-snowflake'
	    }
    }
}

main_app = "django_hinting_cache"
full_name = "django_hinting_cache"
tested_apps = (main_app,)
pip_install_first = True
