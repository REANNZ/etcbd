# -*- coding: utf-8 -*- vim:fileencoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
import os
import warnings
# Marking local settings for translation is not practical, as in
# principle such strings should not be committed to the source file
# (locale/en/LC_MESSAGES/django.po).
# As a workaround translations may be provided in place through a
# dictionary keyed by language. This is applicable only for settings
# to be rendered with 'tolocale' in templates (for example
# NRO_DOMAIN_HELPDESK_DICT). Wrapping such a dictionary with
# djnro.lldict.LazyLangDict ensures that an (arbitrary) string value
# will be returned where a dict is not expected.
from djnro.lldict import LazyLangDict as _ld
from django.utils.translation import gettext_lazy as _
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'djnro')

# override URL settings for XeAP DjNRO
ROOT_URLCONF = 'djnro.urlsextra'

# Override
DATA_DIR = os.path.join(BASE_DIR, 'data')
KML_FILE = os.path.join(DATA_DIR, 'all.kml')

# This should be always False
DEBUG = os.getenv('ADMINTOOL_DEBUG', 'False').upper() == 'TRUE'

# Override LANGUAGES (already set in settings.py) - English only
LANGUAGES = (
    ('en', _('English')),
)
# and apply the same setting to languages available for URLs and names
URL_NAME_LANGS = LANGUAGES

# Set EMAIL_* settings if provided in the environment.
# Note: EMAIL_HOST_USER and EMAIL_HOST_PASSWORD default to empty string, having
# blank values in env file works well here.
# EMAIL_PORT should default to 25 ... but '' gets interpreted correctly - and we set in the default file.
# No need to have overriding logic in a config file
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').upper() == 'TRUE'

ADMINS = (
    # set administrator email address if defined in the environment, otherwise default to original default value
    (os.getenv('ADMIN_USERNAME','admin'), os.getenv('ADMIN_EMAIL','admin@example.org')),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [os.getenv('SITE_PUBLIC_HOSTNAME','*')]
#ALLOWED_HOSTS = ['*']
# Restrict to SITE_PUBLIC_HOSTNAME - or permit any if this variable is not set

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('ADMINTOOL_SECRET_KEY', '<put something really random here, eg. %$#%@#$^2312351345#$%3452345@#$%@#$234#@$hhzdavfsdcFDGVFSDGhn>')

# Google Maps API key, see https://developers.google.com/maps/documentation/javascript/get-api-key#key
# Make this default to None if not set
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_API_KEY', None)

# Check for headers indicating the request was received on a secure SSL connection
# Uncomment this if you are running DjNRO behind an HTTP proxy that sets this
# header for SSL connections (and protects it for non-SSL connections).
SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Protocol', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.getenv('DB_NAME',''),                    # Or path to database file if using sqlite3.
        'USER': os.getenv('DB_USER',''),                    # Not used with sqlite3.
        'PASSWORD': os.getenv('DB_PASSWORD',''),            # Not used with sqlite3.
	# use Docker linking: we get a link to host "postgres"
        'HOST': os.getenv('DB_HOST','postgres'),            # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        #'STORAGE_ENGINE': 'INNODB',
    }
}

STATIC_URL = '/static/'

##### LDAP BACKEND ######
EXTRA_AUTHENTICATION_BACKENDS = (
    # 'django_auth_ldap.backend.LDAPBackend',
)

# LDAP CONFIG

# import ldap
# from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# AUTH_LDAP_BIND_DN = ""
# AUTH_LDAP_BIND_PASSWORD = ""
# AUTH_LDAP_SERVER_URI = "ldap://foo.bar.org"
# AUTH_LDAP_START_TLS = True
# AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People, dc=bar, dc=foo", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

# AUTH_LDAP_USER_ATTR_MAP = {
#       "first_name":"givenName",
#       "last_name": "sn",
#       "email": "mail
#       }

# Set up the basic group parameters.

# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#     "ou=Groups,dc=foo,dc=bar,dc=org",ldap.SCOPE_SUBTREE, objectClass=groupOfNames"
# )

# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_active": "cn=NOC, ou=Groups, dc=foo, dc=bar, dc=org",
#     "is_staff": "cn=staff, ou=Groups, dc=foo, dc=bar, dc=org",
#     "is_superuser": "cn=NOC, ou=Groups,dc=foo, dc=bar, dc=org"
# }


SHIB_AUTH_ENTITLEMENT = ''
FEDERATION_DOC_URL = os.getenv('FEDERATION_DOC_URL', '')
SHIB_LOGOUT_URL = 'https://' + os.getenv('SITE_PUBLIC_HOSTNAME','example.com') + '/Shibboleth.sso/Logout'

SERVER_EMAIL = os.getenv('SERVER_EMAIL',"Example domain eduroam Service <noreply@example.com>")
EMAIL_SUBJECT_PREFIX = "[eduroam] "
ACCOUNT_ACTIVATION_DAYS = 7
NOTIFY_ADMIN_MAILS = [os.getenv('ADMIN_EMAIL','admin@example.org')]

#### CACHE BACKEND ####
# For development instances you can deploy the provided dummy cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'TIMEOUT': 60,
    }
}

# For production instances enable memcache or redis:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#         'TIMEOUT': 60, # default is 300
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# Note: Redis requires the additional pip packages redis and hiredis
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'TIMEOUT': 60, # default is 300
#         'LOCATION': 'redis://127.0.0.1:6379',
#     }
# }

#### SITES FRAMEWORK ####
# You must configure (e.g. via Django admin) your canonical public
# hostname for the site object that matches the SITE_ID configured in
# settings.py or you can add a different object and override it here:
# SITE_ID = 1

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = os.getenv('TIME_ZONE', 'Pacific/Auckland')


# map center (lat, lng)
MAP_CENTER = (os.getenv('MAP_CENTER_LAT', 0.00), os.getenv('MAP_CENTER_LONG', 0.00) )

# Variable used to determine the active Realm object (in views and context processor)
NRO_COUNTRY_CODE = os.getenv('REALM_COUNTRY_CODE', 'tld')
# main domain url used in right top icon, eg. http://www.grnet.gr
# ROID for the active Realm (assigned by eduroam OT)
NRO_ROID = os.getenv('NRO_ROID', NRO_COUNTRY_CODE + '01')
NRO_DOMAIN_MAIN_URL = "http://www.example.com"
# NRO federation name
NRO_FEDERATION_NAME = os.getenv('NRO_FEDERATION_NAME', "NREN AAI federation")
# "provided by" info for footer
NRO_PROV_BY_DICT = {"name": os.getenv('NRO_INST_NAME', "EXAMPLE NRO TEAM"), "url": os.getenv('NRO_INST_URL', "http://noc.example.com")}
# social media contact (Use: // to preserve https)
# Add Facebook and Twitter if set in env vars
NRO_PROV_SOCIAL_MEDIA_CONTACT = [ ] + (
    [ {"url": "//facebook.com/" + os.getenv('NRO_INST_FACEBOOK'), "fa_style":"fa-facebook", "name":"Facebook"} ] if os.getenv('NRO_INST_FACEBOOK') else [] 
    ) + (
    [ {"url": "//twitter.com/" + os.getenv('NRO_INST_TWITTER'), "fa_style":"fa-twitter", "name":"Twitter"} ] if os.getenv('NRO_INST_TWITTER') else [] 
    )

# Helpdesk, used in base.html:
NRO_DOMAIN_HELPDESK_DICT = {"name": _ld({'en':"Domain Helpdesk"}), 'email':'helpdesk@example.com', 'phone': '12324567890', 'uri': 'helpdesk.example.com'}
# realm used to generate a TLS-PSK identity for service providers
NRO_TLSPSK_REALM = os.getenv('NRO_TLSPSK_REALM','set.tlspsk.realm.invalid')

#Countries for Realm model:
REALM_COUNTRIES = (
    (os.getenv('REALM_COUNTRY_CODE','country_2letters'), os.getenv('REALM_COUNTRY_NAME','Country') ),
)

#NRO servers (for Icinga configuration)
# In configuration file, use:
# NRO_SERVERS=server1 server2 ...
# mandatory for each server in NRO_SERVERS:
# NRO_SERVER_HOSTNAME_server1=eduroam1.nren.cc
# NRO_SERVER_HOSTNAME_server2=eduroam2.nren.cc
# NRO_SERVER_SECRET_server1=secret
# NRO_SERVER_SECRET_server2=secret
# optionally also:
# NRO_SERVER_PORT_server1=1812
# NRO_SERVER_PORT_server2=1812
# Is status server enabled?  Set to True if yes, set to False or leave unset if not supported.
# NRO_SERVER_STATUS_server1=True
# NRO_SERVER_STATUS_server2=True
NRO_SERVERS = ()
for s in os.getenv('NRO_SERVERS','').split():
    NRO_SERVERS += tuple([ {
        'name': s,
        'host': os.getenv("NRO_SERVER_HOSTNAME_%s" % (s),''),
        'secret': os.getenv("NRO_SERVER_SECRET_%s" % (s),''),
        'auth_port': os.getenv("NRO_SERVER_PORT_%s" % (s),'1812'),
        'status_server': not os.getenv("NRO_SERVER_STATUS_%s" % (s),'False').upper() in ("FALSE", ""),
        }])

ICINGA_CONF_PARAMS = {
    # Should generated icinga configuration request Chargeable User Identity (CUI)?
    # Set to True if yes, set to False or leave unset if not supported.
    'request_cui': not os.getenv("ICINGA_CONF_REQUEST_CUI",'False').upper() in ("FALSE", ""),
    'operator_name': os.getenv("ICINGA_CONF_OPERATOR_NAME",None),
    'verbosity': os.getenv("ICINGA_CONF_VERBOSITY", "1"),
    # Should attempt to look up IPv6 addresses for radius servers (and include this in Icinga checks)
    # Set to True if yes, set to False or leave unset if not supported.
    'ipv6': not os.getenv("ICINGA_CONF_IPV6", 'False').upper() in ("FALSE", ""),
    # Should generated icinga configuration include direct checks against the institutional servers?
    # Set to True if yes, set to False or blank if not desired
    'generate_instserver_checks': not os.getenv("ICINGA_CONF_GENERATE_INSTSERVER_CHECKS",'True').upper() in ("FALSE", ""),
    # Should generated icinga configuration notify institutional contacts (for server and monitored realm checks?)
    # Set to True if yes, set to False or blank if not desired
    'notify_inst_contacts': not os.getenv("ICINGA_CONF_NOTIFY_INST_CONTACTS",'True').upper() in ("FALSE", ""),
}

RADSECPROXY_CONF_PARAMS = {
    # Top-level domain (to check forwarding)
    'tld': os.getenv("RADSECPROXY_CONF_TLD",None),
}

#TLR servers (for Icinga configuration)
# In configuration file, use:
# TLR_SERVERS=server1 server2 ...
# mandatory for each server in TLR_SERVERS:
# TLR_SERVER_HOSTNAME_server1=eduroam1.tlr
# TLR_SERVER_HOSTNAME_server2=eduroam2.tlr
# TLR_SERVER_SECRET_server1=secret
# TLR_SERVER_SECRET_server2=secret
# optionally also:
# TLR_SERVER_PORT_server1=1812
# TLR_SERVER_PORT_server2=1812
# Is status server enabled?  Set to True if yes, set to False or leave unset if not supported.
# TLR_SERVER_STATUS_server1=True
# TLR_SERVER_STATUS_server2=True

TLR_SERVERS = ()
for s in os.getenv('TLR_SERVERS','').split():
    TLR_SERVERS += tuple([ {
        'name': s,
        'host': os.getenv("TLR_SERVER_HOSTNAME_%s" % (s),''),
        'secret': os.getenv("TLR_SERVER_SECRET_%s" % (s),''),
        'auth_port': os.getenv("TLR_SERVER_PORT_%s" % (s),'1812'),
        'status_server': not os.getenv("TLR_SERVER_STATUS_%s" % (s),'False').upper() in ("FALSE", ""),
        }])

# List the login methods to be offered to users here.
# The fields to list for each method are:
#   backend: backend name.  This has to match the backend name in the
#            corresponding social-auth-core class, or be one of:
#            'shibboleth', 'locallogin'
#   enabled: True or False.  Should this login method be offered to users?
#   class:   Backend class to load.  Gets added to
#            settings.AUTHENTICATION_BACKENDS automatically for enabled login methods.
#   name:    Human readable name of the authentiation method to present to users
#
#   local_image: Relative path of a local static image to use as logo for the login method.
#   image_url:   Full URL of an image to use as logo for the login method.
#   fa_style:    Font-Awesome style to use as logo for the login method.
#
# The first four elements (backend, enabled, class, name) are REQUIRED.
# One of the logo elements (local_image, image_url, fa_style) SHOULD also be provided.
MANAGE_LOGIN_METHODS = (
  { 'backend': 'shibboleth', 'enabled': False, 'class': 'djangobackends.shibauthBackend.shibauthBackend', 'name': 'Shibboleth', 'local_image': 'img/image_shibboleth_logo_color.png' },
  { 'backend': 'locallogin', 'enabled': False, 'class': None, 'name': 'Local login', 'local_image': 'img/right_logo_small.png' },
  # ModelBackend class 'django.contrib.auth.backends.ModelBackend' intentionally omitted as it is always included in AUTHENTICATION_BACKENDS
  { 'backend': 'google-oauth2', 'enabled': True, 'class': 'social_core.backends.google.GoogleOAuth2', 'name': 'Google', 'fa_style': 'fa fa-google fa-2x' },
  { 'backend': 'yahoo-oauth2', 'enabled': True, 'name': 'Yahoo', 'class': 'social_core.backends.yahoo.YahooOAuth2', 'local_image': 'img/yahoo_img.png' },
  { 'backend': 'amazon', 'enabled': False, 'class': 'social_core.backends.amazon.AmazonOAuth2', 'name': 'Amazon', 'fa_style': 'fa fa-amazon fa-2x' },
  { 'backend': 'docker', 'enabled': False, 'class': 'social_core.backends.docker.DockerOAuth2', 'name': 'Docker', 'local_image': 'img/docker-mark-blue.svg' },
  { 'backend': 'dropbox-oauth2', 'enabled': False, 'class': 'social_core.backends.dropbox.DropboxOAuth2V2', 'name': 'Dropbox', 'fa_style': 'fa fa-dropbox fa-2x' },
  { 'backend': 'facebook', 'enabled': False, 'class': 'social_core.backends.facebook.FacebookOAuth2', 'name': 'Facebook', 'fa_style': 'fa fa-facebook fa-2x' },
  { 'backend': 'launchpad', 'enabled': True, 'class': 'social_core.backends.launchpad.LaunchpadOpenId', 'name': 'Launchpad', 'image_url': 'https://login.launchpad.net/assets/identityprovider/img/favicon.ico' },
  { 'backend': 'linkedin-oauth2', 'enabled': False, 'class': 'social_core.backends.linkedin.LinkedinOAuth2', 'name': 'LinkedIn', 'fa_style': 'fa fa-linkedin fa-2x' },
  { 'backend': 'meetup', 'enabled': False, 'name': 'MeetUp', 'class': 'social_core.backends.meetup.MeetupOAuth2', 'image_url': 'http://img1.meetupstatic.com/img/logo.svg' },
  { 'backend': 'twitter', 'enabled': False, 'class': 'social_core.backends.twitter.TwitterOAuth', 'name': 'Twitter', 'fa_style': 'fa fa-twitter fa-2x' },
  # add more here
)

selected_login_methods = os.getenv('ADMINTOOL_LOGIN_METHODS','')
if selected_login_methods:
    # Explicit selection has been made:
    # so enable only methods explicitly listed
    # and disable everything not listed
    selected_login_method_list = selected_login_methods.split()
    for m in MANAGE_LOGIN_METHODS:
        m['enabled'] = ( m['backend'] in selected_login_method_list )

# Add enabled backends to authentication backends
EXTRA_AUTHENTICATION_BACKENDS += tuple([ m['class'] for m in  MANAGE_LOGIN_METHODS if m['enabled'] and m['class'] ])


# Shibboleth attribute map
SHIB_USERNAME = ['HTTP_EPPN']
SHIB_MAIL = ['mail', 'HTTP_MAIL', 'HTTP_SHIB_INETORGPERSON_MAIL']
SHIB_FIRSTNAME = ['HTTP_SHIB_INETORGPERSON_GIVENNAME']
SHIB_LASTNAME = ['HTTP_SHIB_PERSON_SURNAME']
SHIB_ENTITLEMENT = ['HTTP_SHIB_EP_ENTITLEMENT']

# DJANGO SOCIAL AUTH PLUGIN SETTINGS
SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_KEY','')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SECRET','')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = []

for var in os.environ:
    if var.startswith('ADMINTOOL_EXTRA_SETTINGS_'):
        name = var[len('ADMINTOOL_EXTRA_SETTINGS_'):]
        val = os.environ[var]
        try:
            # Special case: handle boolean variables
            if val.upper() == 'TRUE':
                val = True
            elif val.upper() == 'FALSE':
                val = False

            # Note: anything else gets interpreted as string - no chance for data structures to be passed in

            locals()[name] = val  # append list
        except Exception:
            # Not translating because translations not available yet.
            # (And lazy translations are not really suitable for exceptions)
            warnings.warn("Could not import environment variable %s as setting %s with value %s" % ( var, name, val ) )

# SENTRY = {
#     'activate': False,
#     'sentry_dsn': ''
# }

###### eduroam CAT integration ###########
# In order to enable provisioning to CAT, you must list at least one instance and the
# corresponding description in CAT_INSTANCES. Beware that pages accessible by end users
# currently only show CAT information for the instance named 'production'.
# You must also set the following parameters for each CAT instance in CAT_AUTH:
# CAT_API_KEY: Admin API key for authentication to CAT
# CAT_API_URL: Admin API endpoint URL
# CAT_USER_API_URL: User API endpoint URL
# CAT_USER_API_VERSION: User API version
# CAT_USER_API_LOCAL_DOWNLOADS: Base URL for local app downloads (e.g. Android)
# CAT_PROFILES_URL: Base URL for Intitution Download Area pages
# CAT_IDPMGMT_URL: URL For IdP Overview page

# CAT_INSTANCES = (
#     ('production', 'cat.eduroam.org'),
#     ('testing', 'cat-test.eduroam.org'),
# )

# CAT_AUTH = {
#     'production': {
#         "CAT_API_KEY": "<provided API key>",
#         "CAT_API_URL": "https://cat.eduroam.org/admin/API.php",
#         "CAT_USER_API_URL": "https://cat.eduroam.org/user/API.php",
#         "CAT_USER_API_VERSION": 2,
#         "CAT_USER_API_LOCAL_DOWNLOADS": "https://cat.eduroam.org/",
#         "CAT_PROFILES_URL": "https://cat.eduroam.org/",
#         "CAT_IDPMGMT_URL": "https://cat.eduroam.org/admin/overview_org.php"
#     },
#     'testing': {
#         "CAT_API_KEY": "<provided API key>",
#         "CAT_API_URL": "https://cat-test.eduroam.org/admin/API.php",
#         "CAT_USER_API_URL": "https://cat-test.eduroam.org/user/API.php",
#         "CAT_USER_API_VERSION": 2,
#         "CAT_USER_API_LOCAL_DOWNLOADS": "https://cat-test.eduroam.org/",
#         "CAT_PROFILES_URL": "https://cat-test.eduroam.org/",
#         "CAT_IDPMGMT_URL": "https://cat-test.eduroam.org/admin/overview_org.php"
#     },
# }

# CAT User API proxy can optionally cache responses using a Django
# cache backend. By default only expensive API actions (where responses
# are not expected to change frequently) are cached for 10 minutes,
# but a precise cache timeout (in seconds) can be configured for each
# API action, through CAT_USER_API_CACHE_TIMEOUT, per CAT instance.
# Note: For any API call to be cached, if the API response specifies a
# non-zero expiry time, it will be honored by the proxy instead of the
# configured timeout.
# _5m = 5 * 60
# _15m = 15 * 60
# CAT_USER_API_CACHE_TIMEOUT = {
#     'production': {
#         'listAllIdentityProviders': _15m,
#         'listIdentityProviders':    _15m,
#         'orderIdentityProviders':   _15m,
#         'listLanguages':            _15m,
#         'listCountries':            _15m,
#         'listProfiles':              _5m,
#         'listDevices':               _5m,
#         'generateInstaller':        _15m,
#         'profileAttributes':         _5m,
#         'sendLogo':                 _15m,
#         'deviceInfo':                _5m,
#         'detectOS':                 _15m,
#     }
# }

# Parameters for CAT User API proxy, per instance:
# redirect_downloads: Whether download requests should be redirected
#   (this is the default) or proxied to CAT
# allow_cross_origin: Whether CORS headers should be added to
#   responses, so the API proxy may be used by other sites (not by
#   default); can be set to True/False or 'origin'; this setting
#   affects caching, so the cache should be flushed if it is changed
# cache: A specific cache to use (a key from the CACHES setting)
#   rather than the default; set to None to disable caching
# cache_prefix: The key_prefix (see Django @cache_page) that will be
#   used for deriving the cache key (no prefix by default)
# CAT_USER_API_PROXY_OPTIONS = {
#     'production': {
#         'redirect_downloads': True,
#         'allow_cross_origin': False,
#         'cache':              'default',
#         'cache_prefix':       '',
#     }
# }

# Override the template for /connect in order to customize (among other
# things) references specific to cat.eduroam.org for a different CAT
# (production) instance: cat_mailing_list, cat_attribution,
# cat_signed_by etc.
# If this template is stored in djnro/templates/front/cat_connect it
# will already be git-ignored.
# Such a template needs to extend 'front/connect.html' and define blocks
# to be overridden.
# CAT_CONNECT_TEMPLATE = {
#     'production': 'front/cat_connect/connect2.html',
# }
