import re
import socket

from django.shortcuts import redirect, render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseNotFound,
    HttpResponseBadRequest
)
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import gettext as _

from edumanage.models import (
    InstRealmMon,
    Realm,
    InstServer,
    MonLocalAuthnParam,
    Institution,
    InstitutionDetails,
    InstitutionContactPool,
    InstRealm,
    Contact,
)
from edumanage.decoratorsextra import require_ssl, logged_in_or_basicauth, has_perm_or_basicauth


def all_monitoring_contacts():
    """"Return all contacts used in monitoring.  This now means all contacts associated with institutions that are either:
        * Associated with InstRealms that have a monitored realm (InstRealmMon) instance.
        * Have a server associated with the institution
    """

    contacts = set()
    for irm in InstRealmMon.objects.all():
      try:
        for c in irm.realm.instid.institutiondetails.contact.all():
          contacts.add(c)
      except InstitutionDetails.DoesNotExist:
          # If the Institution has no InstitutionDetails, we cannot find any
          # contacts - and in that case, OK to ignore here
          pass

    for server in InstServer.objects.all():
      for inst in server.instid.all():
        try:
          for c in inst.institutiondetails.contact.all():
            contacts.add(c)
        except InstitutionDetails.DoesNotExist:
            # If the Institution has no InstitutionDetails, it is not associated
            # with any contacts - and in that case, OK to ignore here
            pass

    return contacts

def server_addresses(server_names):
    """Return a hash of IPv4 and IPv6 lookups for the given server names.
    """
    server_addr = {}
    for s in server_names:
        s_addr = {}
        # try IPv4 lookup
        try:
            s_ipv4_addr = socket.gethostbyname(s)
            if s_ipv4_addr:
                s_addr['ipv4'] = s_ipv4_addr
        except socket.gaierror:
            # No IPV4 address - pass
            pass
        if settings.ICINGA_CONF_PARAMS['ipv6']:
            # try IPv6 lookup
            try:
                ipv6_addr_info = socket.getaddrinfo(s, None, socket.AF_INET6)
                if len(ipv6_addr_info)>0:
                    # take 1st response, 5th element in 5-tupple is sockaddr, 1st element there is address
                    s_addr['ipv6'] = ipv6_addr_info[0][4][0]
            except socket.gaierror:
                # No IPV6 address - pass
                pass

        server_addr[s] = s_addr
    return server_addr

def icinga_server_addresses():
    """Return a hash of IPv4 and IPv6 lookups for radius servers rendered in Icinga configuration.

    This list covers all NRO servers, plus institutional servers if included in the configuration.
    """
    server_names = [s['host'] for s in settings.NRO_SERVERS]
    if settings.ICINGA_CONF_PARAMS['generate_instserver_checks']:
        server_names += [s.host for s in InstServer.objects.all()]
    return server_addresses(server_names)

@require_ssl
@has_perm_or_basicauth('edumanage.change_monlocalauthnparam',realm='eduroam management tools')
def icingaconf(request):

    resp_body = render_to_string('exports/icinga2.conf',
                    {
                     'allinstrealmmons': InstRealmMon.objects.all(),
                     'nroservers': settings.NRO_SERVERS,
                     'instservers': InstServer.objects.all(),
                     'server_addr': icinga_server_addresses(),
                     'confparams': settings.ICINGA_CONF_PARAMS,
                     'allcontacts': all_monitoring_contacts(),
                    }
                )
    resp_body = re.sub("\n\n\n*","\n\n",
            re.sub(" *$","", resp_body, flags=re.MULTILINE),
            flags=re.MULTILINE)

    resp_content_type = "text/plain"

    return HttpResponse(resp_body,
                        content_type=resp_content_type)



@require_ssl
@has_perm_or_basicauth('edumanage.change_instserver',realm='eduroam management tools')
def radsecproxyconf(request):

    ERTYPES_IDP = [1, 3]
    ERTYPES_SP = [2, 3]

    # client servers: all servers that are affiliated with an institution (and are an SP)
    client_servers = [s for s in InstServer.objects.all() if s.ertype in ERTYPES_SP and s.instid.all()]

    # proxy servers (to be linked with realms): all servers that have a realm (and are an IdP)
    proxy_servers = [s for s in InstServer.objects.all() if s.ertype in ERTYPES_IDP and s.instrealm_set.all()]


    resp_body = render_to_string('exports/radsecproxy.conf',
                    {
                     'institutions': Institution.objects.all(),
                     'client_servers': client_servers,
                     'proxy_servers': proxy_servers,
                     'server_addr': server_addresses([s.host for s in InstServer.objects.all()] +
                                       [s['host'] for s in settings.TLR_SERVERS]),
                     'confparams': settings.RADSECPROXY_CONF_PARAMS,
                     'tlrservers': settings.TLR_SERVERS,
                     'ERTYPES_IDP': ERTYPES_IDP,
                     'ERTYPES_SP': ERTYPES_SP,
                    }
                )
    resp_body = re.sub("\n\n\n*","\n\n",
            re.sub(" *$","", resp_body, flags=re.MULTILINE),
            flags=re.MULTILINE)

    resp_content_type = "text/plain"

    return HttpResponse(resp_body,
                        content_type=resp_content_type)


